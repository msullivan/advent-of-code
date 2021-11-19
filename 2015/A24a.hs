-- This is implemented with a "pruning search monad" that maintains a
-- value based on previously output stuff and can use that to do
-- cutoffs. This is cute but works worse than the thing now
-- implemented for part 2 which is to start with short initial
-- subsequences and work up.

-- For Prune
import Control.Monad
import Control.Monad.Reader
import Control.Monad.ListT
--import Control.Monad.Trans.List
import Data.List.Class

import Data.List
import Data.List.Extra
import Data.Maybe
import qualified Data.Map as Map

------
-- Pruning search monad
type Prune r a = ListT (Reader r) a

pick :: [a] -> Prune r a
pick = fromList

prune :: (a -> Bool) -> Prune a ()
prune f =
  do v <- lift ask
     guard $ f v

runPrune :: (a -> r -> r) -> r -> Prune r a -> [a]
runPrune f v m = run v m
  where run v m = case runReader (runListT m) v of
          Nil -> []
          Cons x xs -> x : run (f x v) xs
------


--partitions :: Eq a => [a] -> [([a], [a])]
partitions cost xs =
  do l <- subsequences xs
     guard $ sum l == cost
     return (l, xs \\ l)

search :: [Int] -> Prune (Int, Int) (Int, Int)
search packages =
  do (a, bc) <- pick $ partitions cost packages
     let v = (length a, product a)
     prune (v<)
     guard $ not $ null $ partitions cost bc
     return v

  where cost = sum packages `div` 3


--pack :: [Int] -> Int
pack packages = search packages

--solve :: String -> Int
solve = runPrune const (100000000,0) . pack . map read . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
