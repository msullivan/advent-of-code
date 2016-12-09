import Data.List.Extra
import Data.Maybe

------
-- Routines I reuse for a lot of problems
answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f
splitOn1 a b = fromJust $ stripInfix a b
--------

decompress ('(':xs) =
  let (lol, ys) = splitOn1 ")" xs
      [n, m] = map read $ splitOn "x" lol
      rep = take n ys
  in (m * (decompress rep)) + decompress (drop n ys)
decompress (x:xs) = 1 + (decompress xs)
decompress [] = 0

main = answer $ decompress . trim
