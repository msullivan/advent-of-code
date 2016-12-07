import Data.List.Extra

answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f

nus [] = ([], [])
nus xs = let (as, bscs) = break (== '[') xs
             (bs, cs) = break (== ']') bscs
             (ys, zs) = nus cs
         in (as ++ ys, bs ++ zs)


check (a:b:c:xs) lol = if a == c && not (a == b) && [b,a,b] `isInfixOf` lol then True
                       else check (b:c:xs) lol
check _ _ = False

check' xs = let (a, b) = nus xs in check a b

main = answer $ length . filter check' . lines
