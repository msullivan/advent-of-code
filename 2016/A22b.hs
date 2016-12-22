import System.IO
import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
import Debug.Trace

------
iread :: String -> Int
iread = read

--answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f
--answer f = interact $ (++"\n") . intercalate "\n" . map show . f

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
type Seen = Map.Map ((Int, Int), (Int, Int)) ()
type Grid = (Map.Map (Int, Int) (Int, Int, Int), (Int, Int), (Int, Int))
loadGrid :: [((Int, Int), (Int, Int, Int))] -> Grid
loadGrid xs =
  let [open] = nub $ map (fst . snd) $ getallviable xs
  in (Map.fromList xs, (maximum $ map (fst . fst) xs, 0), open)

munge [a,b,c,d,e,f] = ((a,b), (c,d,e))

tryMove :: Seen -> Grid -> (Int,Int) -> (Int,Int) -> Maybe Grid
tryMove seen (grid, goal, open) from to = do
  let goal' = if goal == from then to else goal
  let open' = from -- XXXXX:
  guard $ Map.notMember (goal', open') seen
  (ftot, fused, favail) <- Map.lookup from grid
  (ttot, tused, tavail) <- Map.lookup to grid
  guard $ tavail >= fused
  let grid' = Map.insert from (ftot, 0, ftot) $
              Map.insert to (ttot, tused + fused, tavail - fused) grid
  return $ (grid', goal', open')

getMoves :: Seen -> Grid -> (Int,Int) -> [Grid]
getMoves seen grid (to@(x,y)) =
  do (dx,dy) <- [(-1,0),(1,0),(0,-1),(0,1)]
     maybeToList $ tryMove seen grid (x+dx,y+dy) (x,y)

viable (c, (_, used, _)) (c', (_, _, avail)) =
  c /= c' && avail >= used && used > 0

findMatch stuff c = map (\x -> (c,x)) $ filter (viable c) stuff
getallviable ls = concatMap (findMatch ls) ls

maybeTrace b s v = if b then traceShow s v else v

--lol :: Grid -> [Grid]
{-
lol (grid@(rgrid, _, spot)) =
  getMoves grid spot

step state grids = grids :
  let next = filter (\(_,x,y) -> not (Map.member (x,y) state)) $ concatMap lol grids
      state' = foldr (\(_,x,y) m -> Map.insert (x,y) () m) state next
  in traceShow (Map.size state') (step state' next)
-}
search :: Seen -> [(Int,Grid)] -> Int
search seen ((k,grid@(_,goal,open)) : rest) =
  if (0,0) == goal' then k else
    search seen'' $ rest ++ new
  where trans = case rest of [] -> True
                             ((k',_):_) -> k /= k'
        goal' = maybeTrace trans (k, length rest, Map.size seen) goal
        seen' = (Map.insert (goal,open) () seen)
        seen'' = foldr (\(_,(_,g,o)) seen -> Map.insert (g,o) () seen) seen new
        new = do state <- getMoves seen grid open
                 return (k+1, state)


{-
step state grids = grids :
  let next = filter (not . (flip Map.member) state) $ concatMap (nub . lol) grids
      state' = foldr (\k m -> Map.insert k () m) state next
  in step state' next
-}

--
solve grid = search Map.empty [(0,grid)]
{-
solve grid =
  let ass = step Map.empty [grid]
  in  zip [0..] $ map (\x -> (length x, isJust $ find (\(_,s,_) -> s == (0,0)) x)) ass
-}
{-
solve grid =
  let ass = iterate (concatMap (nub . lol)) [grid]
  in zip [0..] $ map (\x -> (length x, isJust $ find (\(_,s,_) -> s == (0,0)) x)) ass
-}

load = loadGrid . map (munge . ireadOut) . lines

main = do hSetBuffering stdout NoBuffering
          answer $ solve . load
--main = answer $ length $ map (munge . ireadOut) . lines
