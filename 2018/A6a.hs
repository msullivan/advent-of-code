import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
import qualified Data.Set as Set

------
iread :: String -> Int
iread = read

do2 f g x = (f x, g x)

answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f

ord0 c = C.ord c - C.ord 'a'
chr0 i = C.chr (i + C.ord 'a')
incletter c i = chr0 ((ord0 c + i) `mod` 26)

splitOn1 a b = fromJust $ stripInfix a b
rsplitOn1 a b = fromJust $ stripInfixEnd a b

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

--------
lpair [x, y] = (x, y)

dist (x0, y0) (x1, y1) = abs (x0 - x1) + abs (y0 - y1)

closest pairs loc = if isNothing other then Just k  else Nothing
  where (v, k) = minimum $ map (\k -> (dist k loc, k)) pairs
        other = find (\other -> dist other loc == v && other /= k) pairs

solve pairs = maximum $ counts
  where offset = 5
        minx = (minimum $ map fst pairs) - offset
        maxx = (maximum $ map fst pairs) + offset
        miny = (minimum $ map snd pairs) - offset
        maxy = (maximum $ map snd pairs) + offset
        infinity = [(x, y) | x <- [minx..maxx], y <- [miny, maxy]] ++
                   [(x, y) | x <- [minx,maxx], y <- [miny..maxy]]
        all = [(x, y) | x <- [minx..maxx], y <- [miny..maxy]]

        infinite = nub $ map (closest pairs) infinity
        all_ds = filter (not . (`elem` infinite)) $ map (closest pairs) all
        counts = map length $ group $ sort all_ds

main = answer $ solve . map lpair . map ireadOut . lines
