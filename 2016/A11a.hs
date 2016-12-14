-- Part B also
-- Does part A in 11s, part B in ~20m

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


--------
type Queue a = ([a], [a])

revApp [] ys = ys
revApp (x:xs) ys = revApp xs (x:ys)

enq (f, b) x = (f, revApp x b)
view ([], []) = Nothing
view (x:xs, b) = Just (x, (xs, b))
view ([], b) = view (reverse b, [])

qFromList x = (x, [])

-------------


stuff = map sort $ [
  ["SG", "SM", "PG", "PM"],
  ["TG", "RG", "RM", "CG", "CM"],
  ["TM"],
  []]

stuff_b = map sort $ [
  ["SG", "SM", "PG", "PM", "EG", "EM", "DG", "DM"],
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

{-
search seen nus = case view nus of
  Just ((k,st), rest) ->
    if done (snd st) then k else
      search seen' $ rest `enq` (next seen (k,st))
    where seen' = Map.insert st () seen
-}
search seen nus = case S.viewl nus of
  (k,st) :< rest ->
    if done (snd st) then k else
      search seen' $ rest >< (S.fromList $ next seen (k,st))
    where seen' = Map.insert st () seen

main = putStrLn $ show $ search Map.empty (S.fromList [(0,(0,stuff_b))])
