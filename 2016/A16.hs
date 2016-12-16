-- both parts

import Data.List.Extra

input = "01111001100111011"

step a =
  let b = map (\x -> if x == '0' then '1' else '0') $ reverse a
  in a ++ "0" ++ b

make a len =
  if length a >= len then a else make (step a) len

cksum' [] = []
cksum' (x:y:xs) = c : cksum' xs
  where c = if x == y then '1' else '0'

cksum s = if even (length s') then cksum s' else s'
  where s' = cksum' s

-- when actually doing it I just poked at things in ghci though
solve len = cksum $ take len $ make input len
main = putStrLn $ show $ (solve 272, solve 35651584)
