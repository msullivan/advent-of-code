import Control.Monad
import Data.List.Extra
import Data.Maybe
import Data.Function
import Data.Bits
import Data.Array as Array
import qualified Data.Char as C
import qualified Data.Map as Map
import qualified Data.Set as Set
import Debug.Trace



------
iread :: String -> Int
iread = read


answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f

splitOn1 a b = fromJust $ stripInfix a b

-- pull out every part of a String that can be read in
-- for some Read a and ignore the rest
readOut :: Read a => String -> [a]
readOut "" = []
readOut s = case reads s of
  [] -> readOut $ tail s
  [(x, s')] -> x : readOut s'
  _ -> error "ambiguous parse"
ireadOut :: String -> [Int]
ireadOut = readOut


replaceAtIndex n item ls = a ++ (item:b) where (a, (_:b)) = splitAt n ls


--------

data Instr' = Iadd | Imul | Iban | Ibor | Iset | Igt | Ieq
  deriving (Enum, Show, Eq, Ord)
type Instr = (Instr', Bool, Bool)

eval_instr' :: Instr' -> Int -> Int -> Int
eval_instr' Iadd = (+)
eval_instr' Imul = (*)
eval_instr' Iban = (.&.)
eval_instr' Ibor = (.|.)
eval_instr' Iset = const
eval_instr' Igt = \x y -> fromEnum $ x > y
eval_instr' Ieq = \x y -> fromEnum $ x == y

step :: (Instr, (Int, Int, Int)) -> [Int] -> [Int]
step ((i, a_imm, b_imm), (a, b, c)) regs =
  let va = if a_imm then a else regs !! a
      vb = if b_imm then b else regs !! b
      res = eval_instr' i va vb
  in replaceAtIndex c res regs

go' i instrs ipreg (ip, regs) =
  let regs' = replaceAtIndex ipreg ip regs
      instr = (Array.!) instrs ip
      regs'' = step instr regs'
      ip' = (regs'' !! ipreg) + 1
  in --traceShow (i, ip, ip', regs', regs'', instr)
     (ip', regs'')

run i instrs ipreg (ip, regs) =
  if ip >= length instrs then (ip, regs)
  else run (i+1) instrs ipreg $ go' i instrs ipreg (ip, regs)


parse [y, z, w] = (y, z, w)

instrs = [(x, x == Iset && y , y) | x <- enumFrom Iadd, y <- [True, False]] ++
         [(Igt, True, False), (Ieq, True, False)]

names = ["addi", "addr", "muli", "mulr", "bani", "banr", "bori", "borr",
         "seti", "setr", "gtri", "gtrr", "eqri", "eqrr", "gtir", "eqir"]
--          "seti", "setr", "gtir", "gtrr", "eqir", "eqrr", "gtri", "eqri"]

imap = Map.fromList $ zip names instrs



solve x = regs !! 0
  where r = head $ ireadOut $ head x
        b = tail x
        ops = map (\z -> ((Map.!) imap $ head $ words z, parse $ ireadOut z)) $ b
        ops' = Array.listArray (0, length ops - 1) ops
        (_, regs) = run 0 ops' r (0, [0, 0, 0, 0, 0, 0])


main = answer $ solve . lines
