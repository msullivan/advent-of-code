-- check critical points
-- test with y, x

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


-- parse = map ((\[x,y] -> (x, y)) . ireadOut)
-- OK THIS PROVES IT WRONG??
-- ALL OF THESE GET IT WRONG

-- aaaaaaa. this is wrong!
parse = map ((\[x,y] -> (x, 1000000-y)) . ireadOut)
-- parse = map ((\[x,y] -> (100-y, x)) . ireadOut)
-- parse = map ((\[x,y] -> (100-x, y)) . ireadOut)
-- parse = map ((\[x,y] -> (y, 100-x)) . ireadOut)

area (x1, y1) (x2, y2) = abs $ (x2-x1+1) * (y2-y1+1)

sort2 (p1, p2) = let [o1, o2] = sort [p1, p2] in (o1, o2)

onLineX ((x1, y1), (x2, y2)) (xi, yi) =
  (x1 == x2 && x2 == xi && y1 <= yi && yi <= y2)
onLineY ((x1, y1), (x2, y2)) (xi, yi) =
  (y1 == y2 && y2 == yi && x1 <= xi && xi <= x2)

onLine seg pi = onLineX seg pi || onLineY seg pi

intersects ((x1, y1), (x2, y2)) ((x3, y3), (x4, y4)) =
  -- maybe right
  (x1 == x2 && y3 == y4 && y1 < y3 && y3 <= y2 && x3 < x1 && x1 <= x4) ||
  (y1 == y2 && x3 == x4 && x1 < x3 && x3 <= x2 && y3 < y1 && y1 <= y4)

inPoly segs p@(x, y) = any (`onLine` p) segs || (count `mod` 2) == 1
  where line = sort2 ((0, y), (x, y))
        count = length $ filter (intersects line) segs


boxlines (x1, y1) (x2, y2) = map sort2 $ zip asdf (tail (asdf ++ asdf))
  where asdf = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]

range' nums a b = filter (\x -> a <= x && x <= b) nums

range nums a b | a <= b = range' nums a b
range nums a b = range' nums b a

points nums ((x1, y1), (x2, y2)) | x1 == x2 = [(x1, y) | y <- range nums y1 y2]
points nums ((x1, y1), (x2, y2))            = [(x, y1) | x <- range nums x1 x2]

boxOK segs nums p1 p2 = all (inPoly segs) ps
  where ls = boxlines p1 p2
        ps = concatMap (points nums) ls
        -- lineok l = not $ any (intersects l) segs

allnums asdf = nub $ sort $ spread
  where flats = concatMap (\(x, y) -> [x, y]) asdf
        spread = concatMap (\x -> [x-1..x+1]) flats

solve m =
  head ok
  -- segs
  -- inPoly segs (9, 3)

  where segs = map sort2 $ zip m (tail (m ++ m))
        nums = allnums m
        best = reverse $ sort [(area a1 a2, a1, a2) | a1 <- m, a2 <- m]
        ok = [n | (n, a1, a2) <- best, boxOK segs nums a1 a2]
        -- , boxOK segs nums a1 a2


main = answer $ solve . parse . lines
