import Data.List
import Data.List.Extra
import Data.Maybe
import qualified Data.Map as Map

solve :: String -> Int
solve = length . filter (\x -> sum x == 150) . subsequences . map read . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
