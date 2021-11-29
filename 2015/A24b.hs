import Control.Monad
import Data.List
import Data.List.Extra
import Data.Maybe
import qualified Data.Map as Map

-- find all subsequences of length n; this lets us search up and find
-- the shortest without ever considering longer ones
subsequences_n :: Int -> [a] -> [[a]]
subsequences_n 0 _ = [[]]
subsequences_n n [] = []
subsequences_n n (x:xs) =
  map (x:) (subsequences_n (n-1) xs) ++ subsequences_n n xs

-- Oh, even better, restrict the sum as we go. This makes it all *really* fast.
subsequences_sum_n 0 0 _ = [[]]
subsequences_sum_n 0 k _ = []
subsequences_sum_n n _ [] = []
subsequences_sum_n _ k _ | k < 0 = []
subsequences_sum_n n k (x:xs) =
  map (x:) (subsequences_sum_n (n-1) (k-x) xs) ++ subsequences_sum_n n k xs

subsequences_sum 0 _ = [[]]
subsequences_sum k _ | k < 0 = []
subsequences_sum _ [] = []
subsequences_sum k (x:xs) =
  map (x:) (subsequences_sum (k-x) xs) ++ subsequences_sum k xs

partitionsBy subs cost xs =
  do l <- subs cost xs
     return (l, xs \\ l)

partitions = partitionsBy subsequences_sum

partitions3 cost l =
  do (a, b) <- partitions cost l
     (b', c) <- partitions cost b
     return (a, b', c)

search :: Int -> [Int] -> [(Int, Int)]
search len packages =
  do (a, bcd) <- partitionsBy (subsequences_sum_n len) cost packages
     guard $ not $ null $ partitions3 cost bcd
     return (length a, product a)

  where cost = sum packages `div` 4

pack :: [Int] -> (Int, Int)
pack packages = go 1
  where go i = case search i packages of
                 [] -> go (i+1)
                 x -> minimum x

solve :: String -> Int
solve = snd . pack . map read . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
