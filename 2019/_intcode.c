/* This was a bad use of my time. */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>
#include <stdlib.h>

/* Apparently there *was* a legit way to do this!
 * Originally "I make own API" to array.array.
 * This will also work for numpy arrays, though calling
 * append won't. */
static int get_buffer(PyObject *array, Py_buffer *buffer,
                      ssize_t *psize, int64_t **pmem)
{
    if (PyObject_GetBuffer(array, buffer,
                           PyBUF_WRITABLE|PyBUF_SIMPLE|PyBUF_FORMAT) == -1) {
        return -1;
    }
    if (strcmp(buffer->format, "q") != 0) {
        PyErr_Format(
            PyExc_TypeError, "invalid array format; needed 'q' but got '%s'",
            buffer->format);
        PyBuffer_Release(buffer);
        return -1;
    }
    *psize = buffer->len / sizeof(int64_t);
    *pmem = buffer->buf;
    return 0;
}


static int grow_array(PyObject *array, Py_buffer *buffer,
                      int amount, ssize_t *psize, int64_t **pmem)
{
    PyBuffer_Release(buffer);

    ssize_t start = Py_SIZE(array);
    amount = amount * 8 / 7;
    // this could be a lot better but I expect it won't come up that much
    for (int i = start; i < amount; i++) {
        PyObject *res = PyObject_CallMethod(array, "append", "i", 0);
        if (!res) return -1;
        Py_DECREF(res);
    }
    return get_buffer(array, buffer, psize, pmem);
}

static int mode_divs[] = { 0, 100, 1000, 10000 };

static int64_t compute_addr(int64_t *mem, int i, int64_t instr, int64_t ip, int64_t relative_base) {
    // XXX: could this be better
    int mode = (instr / mode_divs[i]) % 10;
    int64_t res;
    switch (mode) {
    case 0:
        res = mem[ip+i];
        break;
    case 1:
        res = ip+i;
        break;
    case 2:
        res = mem[ip+i] + relative_base;
        break;
    default:
        PyErr_Format(PyExc_RuntimeError,
                     "Invalid instruction mode %d in instr %d at ip=%d",
                     mode, instr, ip);
        return -1;
    }
    if (res < 0) {
        PyErr_Format(PyExc_RuntimeError,
                     "Invalid negative address %d at ip=%d",
                     res, ip);
    }
    return res;
}

static int64_t read_mem(int64_t *mem, ssize_t size, int64_t addr) {
    return addr >= size ? 0 : mem[addr];
}

#define ADDR(i) ({                                                      \
        int64_t __res = compute_addr(mem, i, instr, ip, relative_base); \
        if (__res < 0) goto err;                                        \
        __res;                                                          \
    })
#define READ(i) read_mem(mem, size, ADDR(i))
#define WRITE(i, v) do {                                                \
        int64_t __addr = ADDR(i);                                       \
        if (__addr >= size) {                                           \
            if (grow_array(program, &buffer, __addr, &size, &mem) < 0)  \
                goto err;                                               \
        }                                                               \
        mem[__addr] = (v);                                              \
    } while (0)


static int
_execute_intcode(PyObject *program,
                 int64_t *p_ip, int64_t *p_relative_base,
                 PyObject *input, PyObject *output,
                 int64_t *p_max_instrs)
{
    Py_buffer buffer = { .buf = NULL };
    ssize_t size;
    int64_t *mem;

    if (get_buffer(program, &buffer, &size, &mem) < 0) goto err;

    int64_t ip = *p_ip;
    int64_t relative_base = *p_relative_base;
    int64_t cnt = 0;
    int64_t max_instrs = *p_max_instrs;
    int res;
    PyObject *obj;

    while (ip >= 0) {
        if (ip + 4 >= size) {
            if (grow_array(program, &buffer, ip + 4, &size, &mem) < 0) goto err;
        }
        if (max_instrs && cnt++ > max_instrs) break;

        int64_t instr = mem[ip];

        switch (instr % 100) {
        case 1:
            WRITE(3, READ(1) + READ(2));
            ip += 4;
            break;
        case 2:
            WRITE(3, READ(1) * READ(2));
            ip += 4;
            break;
        case 3: {
            if ((res = PyObject_IsTrue(input)) < 0) goto err;
            if (!res)
                goto out; /* queue empty */
            if (!(obj = PyObject_CallMethod(input, "pop", "i", 0))) goto err;
            int64_t val = PyLong_AsLongLong(obj);
            Py_DECREF(obj);
            if (val == -1 && PyErr_Occurred()) goto err;
            WRITE(1, val);
            ip += 2;
            break;
        }
        case 4:
            if (!(obj = PyObject_CallMethod(output, "append", "L", READ(1)))) goto err;
            Py_DECREF(obj);
            ip += 2;
            break;
        case 5:
            if (READ(1) != 0) {
                ip = READ(2);
            } else {
                ip += 3;
            }
            break;
        case 6:
            if (READ(1) == 0) {
                ip = READ(2);
            } else {
                ip += 3;
            }
            break;
        case 7:
            WRITE(3, READ(1) < READ(2));
            ip += 4;
            break;
        case 8:
            WRITE(3, READ(1) == READ(2));
            ip += 4;
            break;
        case 9:
            relative_base += READ(1);
            ip += 2;
            break;
        case 99:
            ip = -1;
            break;
        default:
            PyErr_Format(PyExc_RuntimeError, "Invalid instruction %d at ip=%d", instr, ip);
            goto err;
        }

    }
out:

    PyBuffer_Release(&buffer);

    *p_ip = ip;
    *p_relative_base = relative_base;
    *p_max_instrs = cnt;

    return 0;

err:
    PyBuffer_Release(&buffer);
    return -1;
}

static PyObject *
execute_intcode(PyObject *self, PyObject *args)
{
    PyObject *program, *input, *output;
    int64_t ip, relative_base, max_instrs;

    if (!PyArg_ParseTuple(
            args, "OLLOOL", &program, &ip, &relative_base, &input, &output, &max_instrs))
        return NULL;

    int res = _execute_intcode(program, &ip, &relative_base, input, output, &max_instrs);
    if (res < 0)
        return NULL;

    return Py_BuildValue("iii", ip, relative_base, max_instrs);
}

static PyMethodDef _intcode_methods[] = {
    {"execute_intcode", execute_intcode, METH_VARARGS,\
     "Run an intcode program."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef _intcode_module = {
    PyModuleDef_HEAD_INIT,
    "_intcode",
    NULL,
    -1,
    _intcode_methods,
};

PyMODINIT_FUNC
PyInit__intcode(void)
{
    PyObject *m;

    m = PyModule_Create(&_intcode_module);
    if (m == NULL)
        return NULL;

    return m;
}
