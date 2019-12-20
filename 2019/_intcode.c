/* This was a bad use of my time. */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>
#include <stdlib.h>

/* There isn't a C API for array.array so I make own API. */
typedef struct arrayobject {
    PyObject_VAR_HEAD
    char *ob_item;
} arrayobjectprefix;

#define _get_array(o) ((int64_t *)((arrayobjectprefix *)o)->ob_item)

static int grow_array(PyObject *array, int amount, ssize_t *psize, int64_t **pmem)
{
    ssize_t start = Py_SIZE(array);
    amount = amount * 8 / 7;
    // this could be a lot better but I expect it won't come up that much
    for (int i = start; i < amount; i++) {
        PyObject *res = PyObject_CallMethod(array, "append", "i", 0);
        if (!res) return -1;
        Py_DECREF(res);
    }
    *psize = Py_SIZE(array);
    *pmem = _get_array(array);
    return 0;
}

static int mode_divs[] = { 0, 100, 1000, 10000 };

static int64_t compute_addr(int64_t *mem, int i, int64_t instr, int64_t ip, int64_t relative_base) {
    // XXX: could this be better
    int mode = (instr / mode_divs[i]) % 10;
    switch (mode) {
    case 0:
        return mem[ip+i];
    case 1:
        return ip+i;
    case 2:
        return mem[ip+i] + relative_base;
    }
    abort();
}

static int64_t read_mem(int64_t *mem, ssize_t size, int64_t addr) {
    return addr < 0 || addr >= size ? 0 : mem[addr];
}

#define ADDR(i) compute_addr(mem, i, instr, ip, relative_base)
#define READ(i) read_mem(mem, size, ADDR(i))
#define WRITE(i, v) do {                                        \
        int64_t __addr = ADDR(i);                               \
        if (__addr >= size) {                                   \
            if (grow_array(program, __addr, &size, &mem) < 0)   \
                return -1;                                      \
        }                                                       \
        mem[__addr] = (v);                                      \
    } while (0)


static int
_execute_intcode(PyObject *program,
                 int64_t *p_ip, int64_t *p_relative_base,
                 PyObject *input, PyObject *output)
{
    ssize_t size = Py_SIZE(program);
    int64_t *mem = _get_array(program);
    int64_t ip = *p_ip;
    int64_t relative_base = *p_relative_base;
    int res;
    PyObject *obj;

    while (ip >= 0) {
        if (ip + 4 >= size) {
            if (grow_array(program, ip + 4, &size, &mem) < 0)
                return -1;
        }

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
            if ((res = PyObject_IsTrue(input)) < 0) return -1;
            if (!res)
                goto out; /* queue empty */
            if (!(obj = PyObject_CallMethod(input, "pop", "i", 0))) return -1;
            int64_t val = PyLong_AsLongLong(obj);
            Py_DECREF(obj);
            if (val == -1 && PyErr_Occurred()) return -1;
            WRITE(1, val);
            ip += 2;
            break;
        }
        case 4:
            if (!(obj = PyObject_CallMethod(output, "append", "L", READ(1)))) return -1;
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
            return -1;
        }

    }
out:

    *p_ip = ip;
    *p_relative_base = relative_base;

    return 0;
}

static PyObject *
execute_intcode(PyObject *self, PyObject *args)
{
    PyObject *program, *input, *output;
    int64_t ip, relative_base;

    if (!PyArg_ParseTuple(args, "OLLOO", &program, &ip, &relative_base, &input, &output))
        return NULL;

    int res = _execute_intcode(program, &ip, &relative_base, input, output);
    if (res < 0)
        return NULL;

    return Py_BuildValue("ii", ip, relative_base);
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
