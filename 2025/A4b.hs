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

vadd (x1, y1) (x2, y2) = (x1+x2, y1+y2)
dirs = [(dx, dy) | dx <- [-1..1], dy <- [-1..1], dx /= 0 || dy /= 0]


parse :: [[a]] -> Map.Map (Int, Int) a
-- parse :: [[a]] -> [((Int, Int), a)]
parse lines =
  Map.fromList $
  concat $ zipWith (\l y -> zipWith (\c x -> ((x, y), c)) l [0..]) lines [0..]

step m = (foldr Map.delete m todel, length todel)
  where todel = filter ok (Map.keys m)
        ok pos = Map.lookup pos m == Just '@' && (length $ filter hasNbr dirs) < 4
          where hasNbr dir = Map.findWithDefault '.' (vadd pos dir) m == '@'

solve m =
  let (m', n) = step m
  in
    if n == 0 then 0
    else n + solve m'

main = answer $ solve . parse . lines
