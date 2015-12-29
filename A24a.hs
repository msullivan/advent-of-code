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

type Prune r a = ListT (Reader (Maybe r)) a

--pick :: [a] -> Prune a
pick = fromList

prune :: (a -> Bool) -> Prune a ()
prune f =
  do v <- lift ask
     case v of
       Nothing -> return ()
       Just v' -> guard $ f v'

runPrune :: Prune a a -> [a]
runPrune m = run Nothing m
  where run v m = case runReader (runListT m) v of
          Nil -> []
          Cons x xs -> x : run (Just x) xs


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
solve = runPrune . pack . map read . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
