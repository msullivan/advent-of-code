-- For Prune
import Control.Monad
import Control.Monad.Reader
import Control.Monad.RWS
import Control.Monad.ListT
import Data.List.Class
--
import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
--
import qualified Data.Sequence as S
import Data.Sequence ((<|), (|>), (><), ViewL(..))


import Debug.Trace

------
iread :: String -> Int
iread = read

answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f

ord0 c = C.ord c - C.ord 'a'
chr0 i = C.chr (i + C.ord 'a')
incletter c i = chr0 ((ord0 c + i) `mod` 26)

splitOn1 a b = fromJust $ stripInfix a b
rsplitOn1 a b = fromJust $ stripInfixEnd a b

-- Pruning search monad
type Prune s r a = ListT (RWS r () s) a

pick :: [a] -> Prune s r a
pick = fromList

prune :: (a -> Bool) -> Prune s a ()
prune f =
  do v <- lift ask
     guard $ f v

runPrune :: (a -> r -> r) -> s -> r -> Prune s r a -> [a]
runPrune f s v m = run s v m
  where run s v m = case runRWS (runListT m) v s of
          (Nil, _, _) -> []
          (Cons x xs, s, _) -> x : run s (f x v) xs
------

--------


stuff = map sort $ [
  ["SG", "SM", "PG", "PM"],
  ["TG", "RG", "RM", "CG", "CM"],
  ["TM"],
  []]

stuff' = map sort $ [
  ["HM", "LM"],
  ["HG"],
  ["LG"],
  []]

stuff'' = map sort $ [
  ["HM", "HG"],
  [],
  [],
  []]

oneThings xs =
  do x <- xs
     return [x]
twoThings xs =
  do x <- xs
     y <- xs \\ [x]
     return [x, y]
things xs = oneThings xs ++ twoThings xs

replaceAtIndex n item ls = a ++ (item:b) where (a, (_:b)) = splitAt n ls

thingsmatch (x:"M") (y:"G") = x == y
thingsmatch _ _ = False
thingsbreak (x:"M") (y:"G") = x /= y
thingsbreak _ _ = False

linesafe xs = all (\x -> if (x !! 1) == 'M' then
                           any (thingsmatch x) xs || not (any (thingsbreak x) xs)
                         else True) xs

done [[], [], [], _] = True
done _ = False


next :: Table -> (Int, (Int, [[String]])) -> [(Int, (Int, [[String]]))]
next map (k, (i, state)) =
  do guard $ Map.notMember (i, state) map
     let xs = state !! i
     parts <- things xs
     i' <- [i-1, i+1]
     guard $ i' >= 0 && i' <= 3
--     guard $ length parts == 1 || i' == i+1
     let state' = replaceAtIndex i (xs \\ parts) (replaceAtIndex i' (sort (parts ++ (state !! i'))) state)
     guard $ all linesafe state'
     guard $ Map.notMember (i', state') map
     return (k+1, traceA (map, (i', state')) (i', state'))

type Table = Map.Map (Int, [[String]]) ()
traceNus x = traceShow x x
--traceA = traceShow
traceA a b = b


search seen nus = case S.viewl nus of
  (k,st) :< rest ->
    if done (snd st) then k else
      search seen' $ rest >< (S.fromList $ next seen (k,st))
    where seen' = Map.insert st () seen


main = putStrLn $ show $ search Map.empty (S.fromList [(0,(0,stuff))])
