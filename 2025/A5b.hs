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


parse lines =
  let [ranges, nums] = splitOn [[]] lines
  in (map ((\[x, y] -> (x, -y)) . ireadOut) ranges, map iread nums)

inrange i (lo, hi) = lo <= i && i <= hi

merge [] = []
merge [x] = [x]
merge ((l1, h1):(l2, h2):rest) =
  if l2 <= h1
  then
    merge ((l1, max h1 h2):rest)
  else
    (l1, h1) : merge ((l2, h2):rest)

size (l, h) = h - l + 1

solve (ranges, nums) =
  sum $ map size $ merge $ sort ranges

main = answer $ solve . parse . lines
