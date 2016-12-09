import Data.List.Extra
import Data.Maybe
import Control.Monad
import qualified Data.Sequence as S
import Data.Sequence ((<|), (><))

-- This is a version of 9 part two that actually *does* kind of
-- construct the string. It does it using a Data.Sequence which can
-- efficiently operate on big lazy things.

-- It is structured exactly like producing the list would be except it
-- calls equivalent Sequence functions. It runs basically instantly
-- and can be made to generate text. You can ask it for the expansion
-- at basically any point in the string and it will return data very
-- quickly!

------
answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f
splitOn1 a b = fromJust $ stripInfix a b
--------

decompress ('(':xs) =
  let (lol, ys) = splitOn1 ")" xs
      [n, m] = map read $ splitOn "x" lol
      (rep, rest) = splitAt n ys
  in join (S.replicate m (decompress rep)) >< decompress rest
decompress (x: xs) = x <| decompress xs
decompress [] = S.empty

-- You can do things like this!
--main = answer $ S.drop 9000000000 . decompress . trim
main = answer $ S.length . decompress . trim
