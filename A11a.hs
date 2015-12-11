import Data.List
import Data.Char

incletter c i = chr (ord c + i)
letter = incletter 'a'

doubles = [ [c, c] | i <- [0..25], let c = letter i ]
runs = [ [letter i, letter (i+1), letter (i+2)] | i <- [0..23] ]
noneof = ["i", "o", "l"]

increv ('z' : xs) = 'a' : increv xs
increv (c : xs) = incletter c 1 : xs

inc = reverse . increv . reverse

matches s = hasDoubles && hasRun && notBad
  where hasDoubles = length (filter (`isInfixOf` s) doubles) >= 2
        hasRun = any (`isInfixOf` s) runs
        notBad = not $ any (`isInfixOf` s) noneof

-- Again, I actually just ran this in ghci. Outputs both of the answers.
input = "hepxcrrq"
main = putStrLn $ show $ take 2 $ filter matches $ iterate inc input
