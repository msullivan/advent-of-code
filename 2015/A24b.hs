import Control.Monad
import Data.List
import Data.List.Extra
import Data.Maybe
import qualified Data.Map as Map

--partitions :: Eq a => [a] -> [([a], [a])]
partitions cost xs =
  do l <- subsequences xs
     guard $ sum l == cost
     return (l, xs \\ l)

--partitions3 :: Eq a => [a] -> [([a], [a], [a])]
partitions3 cost l =
  do (a, b) <- partitions cost l
     (b', c) <- partitions cost b
     return (a, b', c)

--search :: [Int] -> Int
search packages =
  do (a, bcd) <- partitions cost packages
     guard $ length a <= 5 -- garbage
     guard $ not $ null $ partitions3 cost bcd
     return (length a, product a)

  where cost = sum packages `div` 4

--pack :: [Int] -> Int
pack packages = search packages

--solve :: String -> Int
solve = snd . minimum . pack . map read . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
