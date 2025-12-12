import Control.Monad
import Data.List
import Data.List.Split
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
import qualified Data.Set as Set
import Debug.Trace

------
iread :: String -> Int
iread = read

do2 f g x = (f x, g x)

answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f

ord0 c = C.ord c - C.ord 'a'
chr0 i = C.chr (i + C.ord 'a')
incletter c i = chr0 ((ord0 c + i) `mod` 26)

-- splitOn1 a b = fromJust $ stripInfix a b
-- rsplitOn1 a b = fromJust $ stripInfixEnd a b

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

traceShow' s = traceShow s s

--------

droplast l = take (length l - 1) l

parse1 l = (target', nums', jolts)
  where (target:nums) = splitOn " " l
        inums = map ireadOut nums
        nums' = droplast inums
        jolts = last inums
        target' = map (=='#') (tail $ droplast $ target)

parse lines = map parse1 lines

step :: [Int] -> [Bool] -> [Bool]
step buttons state = zipWith (\b i -> if i `elem` buttons then not b else b) state [0..]

search :: ([Bool], [[Int]], [Int]) -> Int
search (target, buttons, _) =
  minimum $ concatMap try $ subsequences buttons
  where
    start = map (const False) target
    try :: [[Int]] -> [Int]
    try sub = if foldr step target sub == start then [length sub] else []



solve m = sum $ map search m

main = answer $ solve . parse . lines
