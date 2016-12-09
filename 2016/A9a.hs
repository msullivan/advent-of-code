import Data.List.Extra
import Data.Maybe

------
answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f
splitOn1 a b = fromJust $ stripInfix a b
--------

decompress ('(':xs) =
  let (lol, ys) = splitOn1 ")" xs
      [n, m] = map read $ splitOn "x" lol
      rep = take n ys
  in concat (replicate m rep) ++ decompress (drop n ys)
decompress (x:xs) = x : decompress xs
decompress [] = []

main = answer $ length . decompress . trim
