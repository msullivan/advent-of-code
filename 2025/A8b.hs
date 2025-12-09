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
-- dirs = [(dx, dy) | dx <- [-1..1], dy <- [-1..1], dx /= 0 || dy /= 0]
shifts = [(-1, 0), (1, 0)]
down = (0, 1)


-- parse = map ((\[a,b,c] -> (a,b,c)) . ireadOut)
parse = map ireadOut
mag2 v = sum $ zipWith (*) v v
dist2 x y = mag2 $ zipWith (-) x y



type UnionFind a = Map.Map a a

uf_empty = Map.empty

canon m x =
  case Map.lookup x m of
    Nothing -> x
    Just x' | x == x' -> x
    Just x' -> canon m x'

uf_union m x y =
  let x' = canon m x
      y' = canon m y
  in Map.insert x x' $ Map.insert y' x' $ Map.insert y x' m

solve d = head out
  -- product $
  -- take 10 $ reverse $ sort $ map snd $ Map.toList grp_sizes
  where
    ps = sortOn snd [((x, y), dist2 x y) | x <- d, y <- d, x < y]
    (_, grps) = mapAccumL step uf_empty ps
    step m ((x, y), _) = (m', ((x, y), m'))
      where m' = uf_union m x y
    num_groups m = length $ Set.fromList $ map (canon m) d

    out = [head x * head y | ((x, y), m) <- grps, num_groups m == 1]



main = answer $ solve . parse . lines
