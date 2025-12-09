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


parse :: [[a]] -> Map.Map (Int, Int) a
-- parse :: [[a]] -> [((Int, Int), a)]
parse lines =
  Map.fromList $
  concat $ zipWith (\l y -> zipWith (\c x -> ((x, y), c)) l [0..]) lines [0..]

drop1 m (v, cnt) =
  let v' = vadd v down
  in Map.fromList $ map (,cnt) $ case Map.lookup v m of
    Just 'S' -> [(v')]
    Just '.' -> [(v')]
    Just '^' -> [vadd v' s | s <- shifts]
    _ -> []

go m frontier =
  let nf = foldr (Map.unionWith (+)) Map.empty $ map (drop1 m) $ Map.toList frontier
  in if Map.null nf then frontier
     else (go m nf)

solve m = sz
  where all = go m (Map.fromList start)
        start = [(k, 1) | (k, v) <- Map.toList m, v == 'S']
        sz = sum [cnt | (_, cnt) <- Map.toList all]
        -- sz = length [v | v <- Set.toList all, Map.lookup v m == Just '^']

main = answer $ solve . parse . lines
