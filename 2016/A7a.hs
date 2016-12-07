import Data.List.Extra

answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f

check nus ('[':xs) = check (not nus) xs
check nus (']':xs) = check (not nus) xs
check nus (a:b:c:d:xs) | nus && a == d && b == c && not (a == b) = True
                       | otherwise = check nus (b:c:d:xs)
check nus _ = False

check' xs = check True xs && not (check False xs)

main = answer $ length . filter check' . lines
