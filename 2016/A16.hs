-- both parts

import Data.List.Extra
import Data.Char

input = map digitToInt "01111001100111011"

step a =
  let b = map (1-) $ reverse a
  in a ++ [0] ++ b

make a len = until ((len <=) . length) step a

cksum' [] = []
cksum' (x:y:xs) = c : cksum' xs
  where c = if x == y then '1' else '0'

cksum = until (odd . length) cksum' . cksum'

-- when actually doing it I just poked at things in ghci though
solve len = cksum $ take len $ make input len
main = putStrLn $ show $ (solve 272, solve 35651584)
