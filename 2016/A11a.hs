-- XXX: doesn't work at all

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


next :: (Int, [[String]]) -> [(Int, [[String]])]
next (i, state) =
  do let xs = state !! i
     parts <- things xs
     i' <- [i-1, i+1]
     guard $ i' >= 0 && i' <= 3
     guard $ length parts == 1 || i' == i+1
     let state' = replaceAtIndex i (xs \\ parts) (replaceAtIndex i' (sort (parts ++ (state !! i'))) state)
     guard $ all linesafe state'
     return (i', state')

type Table = Map.Map (Int, [[String]]) Int
traceNus x = traceShow x x
--traceA = traceShow
traceA a b = b


search :: (Int, [[String]]) -> Int -> Prune Table Int Int
search st k =
  if done (snd st) then return (k) else
  do m <- lift get
     let m' = Map.insert st k m
     lift $ put m'
     prune ((k+1)<)
     st' <- pick $ next st
     guard $ (fromMaybe 1000000000 (Map.lookup st' m')) > k
     search (traceA (k, st') st') (k+1)


solve lol k = runPrune (\x y -> x) Map.empty (k :: Int) $ search (0, lol) 0


    {-
load = map iread . words

main = answer $ length . filter check . map load . lines
-}
