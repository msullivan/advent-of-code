import System.IO
import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Set as Set
import qualified Data.Map as Map
import Debug.Trace
import Control.Arrow

------
iread :: String -> Int
iread = read

--answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f
--answer f = interact $ (++"\n") . intercalate "\n" . map show . f

--------
type Pos = (Int, Int)
type Seen = Set.Set Pos
type Grid = Set.Set Pos

maybeTrace b s v = if b && False then traceShow s v else v

search :: Pos -> Grid -> Seen -> [(Int,Pos)] -> Int
search goal grid seen ((k,pos) : rest) =
  if goal' == pos then k else
    search goal grid seen' $ rest ++ new
  where trans = case rest of [] -> True
                             ((k',_):_) -> k /= k'
        goal' = maybeTrace trans (k, length rest, Set.size seen) goal
        seen' = foldr Set.insert seen (map snd new)
        new = do state <- getMoves seen grid pos
                 return (k+1, state)

searchS :: Pos -> Grid -> Pos -> Int
searchS goal grid start =
  search goal grid (Set.singleton start) [(0,start)]

getMoves :: Seen -> Grid -> Pos -> [Pos]
getMoves seen grid (from@(x,y)) =
  do (dx,dy) <- [(-1,0),(1,0),(0,-1),(0,1)]
     let to = (x+dx,y+dy)
     guard $ Set.notMember to seen
     guard $ Set.member to grid
     return to

--

label :: [[a]] -> [(a,(Int,Int))]
label = concat . zipWith (\i -> zipWith (\j c -> (c,(i,j))) [0..]) [0..]

allpairs open nums =
  do (i,from) <- nums
     (j,to) <- nums
     return $ ((from,to), searchS to open from)

load locs = (nums, dists)
  where open = Set.fromList $ map snd $ filter ((/='#') . fst) locs
        nums = map (\(x,y) -> (C.digitToInt x, y)) $ filter ((/='.') . fst) $ filter ((/='#') . fst) locs
        dists = allpairs open nums

pathlen dists path = sum $ map (fromJust . (flip lookup) dists) pairs
  where pairs = zip path (tail path)

solve (nums, dists) =
  let (start:rest) = map snd $ sort nums
      perms = map (start:) $ permutations rest
  in minimum $ map (pathlen dists) perms
solve' (nums, dists) =
  let (start:rest) = map snd $ sort nums
      perms = map (\x -> start:x++[start]) $ permutations rest
  in minimum $ map (pathlen dists) perms

main = do hSetBuffering stdout NoBuffering
          answer $ (solve &&& solve') . load . label . lines
--main = answer $ length $ map (munge . ireadOut) . lines
