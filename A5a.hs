import Data.List
import Data.Char


vowels = "aeiou"
doubles = [ [c, c] | i <- [0..25], let c = chr (ord 'a' + i) ]
bad = ["ab", "cd", "pq", "xy"]

good s = hasVowels && hasDoubles && notBad
  where hasVowels = length (filter (`elem` vowels) s) >= 3
        hasDoubles = any (`isInfixOf` s) doubles
        notBad = not $ any (`isInfixOf` s) bad

answer f = interact $ (++"\n") . show . f
main = answer $ length . filter good . lines
