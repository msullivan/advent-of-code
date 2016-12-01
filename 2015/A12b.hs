import Data.List
import Data.List.Extra
import Text.JSON

-- I wrote the python one first but wanted to see how nice doing it in
-- haskell would have been.
-- need to: cabal install json

process :: JSValue -> Int
process (JSRational _ i) = ceiling i
process (JSArray ls) = sum $ map process ls
process (JSObject ls) =
  if any (\ (_, v) -> encode v == encode "red") alist then 0 else
    sum $ map process $ map snd alist

  where alist = fromJSObject ls
process _ = 0

solve :: String -> Int
solve input = process res
  where Ok res = decode input

answer f = interact $ (++"\n") . show . f
main = answer solve
