import Data.List
import Data.List.Extra
import Data.Maybe
import qualified Data.Map as Map

nus a =
  let x = minimum $ map length a
      b = filter (\z -> length z == x) a
  in length b

solve :: String -> Int
solve = nus . filter (\x -> sum x == 150) . subsequences . map read . lines

answer f = interact $ (++"\n") . show . f
main = answer solve
