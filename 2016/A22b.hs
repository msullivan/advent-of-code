import System.IO
import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map

------
iread :: String -> Int
iread = read

--answer :: (Show a) => (String -> a) -> IO ()
--answer f = interact $ (++"\n") . show . f
answer f = interact $ (++"\n") . intercalate "\n\n" . map show . f

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

type Grid = (Map.Map (Int, Int) (Int, Int, Int), (Int, Int))
loadGrid :: [((Int, Int), (Int, Int, Int))] -> Grid
loadGrid xs = (Map.fromList xs, (maximum $ map (fst . fst) xs, 0))

munge [a,b,c,d,e,f] = ((a,b), (c,d,e))

tryMove :: Grid -> (Int,Int) -> (Int,Int) -> Maybe Grid
tryMove (grid, goal) from to = do
  (ftot, fused, favail) <- Map.lookup from grid
  (ttot, tused, tavail) <- Map.lookup to grid
  guard $ tavail >= fused
  let grid' = Map.insert from (ftot, 0, ftot) $
              Map.insert to (ttot, tused + fused, tavail - fused) grid
  let goal' = if goal == from then to else goal
  return $ (grid', goal')

getMoves :: Grid -> (Int,Int) -> [Grid]
getMoves grid (from@(x,y)) =
  do (dx,dy) <- [(-1,0),(1,0),(0,-1),(0,1)]
     maybeToList $ tryMove grid (x,y) (x+dx,y+dy)

viable (c, (_, used, _)) (c', (_, _, avail)) =
  c /= c' && avail >= used && used > 0

findMatch stuff c = map (\x -> (c,x)) $ filter (viable c) stuff
getallviable ls = concatMap (findMatch ls) ls

lol :: Grid -> [Grid]
lol (grid@(rgrid, _)) =
  concatMap (getMoves grid) (Map.keys rgrid)

step state grids = grids :
  let next = filter (not . (flip Map.member) state) $ concatMap (nub . lol) grids
      state' = foldr (\k m -> Map.insert k () m) state next
  in step state' next

{-
step state grids = grids :
  let next = filter (not . (flip Map.member) state) $ concatMap (nub . lol) grids
      state' = foldr (\k m -> Map.insert k () m) state next
  in step state' next
-}

solve grid =
  let ass = step Map.empty [grid]
  in zip [0..] $ map (\x -> (length x, isJust $ find (\(_,s) -> s == (0,0)) x)) ass

     {-
solve grid =
  let ass = iterate (concatMap (nub . lol)) [grid]
  in zip [0..] $ map (\x -> (length x, isJust $ find (\(_,s) -> s == (0,0)) x)) ass
-}

load = loadGrid . map (munge . ireadOut) . lines

main = do hSetBuffering stdout NoBuffering
          answer $ solve . load
--main = answer $ length $ map (munge . ireadOut) . lines
