import Control.Monad
import Data.List.Extra
import Data.Maybe

elf n = e
  where e = n*10 : replicate (n-1) 0 ++ e
elves n =
  zipWith (+) (elf n) (0 : elves (n+1))

presents n =
  sum [if n `mod` i == 0 then i*10 else 0 | i <- [1..n `div` 2]] + (n*10)

-- This is vastly too slow.
