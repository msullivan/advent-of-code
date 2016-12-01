import Data.List
import Data.List.Extra
import Data.Maybe
import qualified Data.Map as Map

countMinConfigs l =
  let min = minimum $ map length l
  in length $ filter (\z -> length z == min) l

solve :: String -> Int
solve = countMinConfigs . filter (\x -> sum x == 150) . subsequences .
        map read . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
