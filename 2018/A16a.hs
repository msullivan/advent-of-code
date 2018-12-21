import Control.Monad
import Data.List.Extra
import Data.Maybe
import Data.Bits
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

parse [x, y, z, w] = (x, (y, z, w))

instrs = [(x, x == Iset && y , y) | x <- enumFrom Iadd, y <- [True, False]] ++
         [(Igt, True, False), (Ieq, True, False)]

couldMatch (before:instr:after:_) = length res
  where (_, args) = parse instr
        res = filter (\i -> step (i, args) before == after) instrs

solve x = length $ filter (>=3) stuff
  where stuff = map couldMatch $ chunksOf 4 x

main = answer $ solve . fst . splitOn1 [[], [], []] . map ireadOut . lines
