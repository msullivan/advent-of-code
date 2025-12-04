module Memoize where

import Data.List

class Memoize a where
  memoize :: (a -> v) -> a -> v

memoFix :: Memoize a => ((a -> v) -> a -> v) -> a -> v
memoFix ff = f
  where f = memoize (ff f)

--

-- Core memoization primitives for unit, product, and sums.

-- All of my other implementations work by coercing values into these
-- types and back.

instance Memoize () where
  -- We memoize () by binding its unique result to a variable, and
  -- then reusing that
  memoize f = mf
    where v = f ()
          mf () = v

instance (Memoize a, Memoize b) => Memoize (a, b) where
  memoize f = mf
    -- We memoize a product by memoizing the elements individually
    where fc = memoize $ \xa -> memoize $ \xb -> f (xa, xb)
          mf (xa, xb) = fc xa xb

instance (Memoize a, Memoize b) => Memoize (Either a b) where
  memoize f = mf
    -- We memoize a sum by memoizing the left and right cases in
    -- saved variables, and then dispatching to the appropriate one.
    where fl = memoize $ \x -> f (Left x)
          fr = memoize $ \x -> f (Right x)

          mf (Left x) = fl x
          mf (Right x) = fr x


----

instance Memoize Bool where
  -- Bool <=> Either () ()
  memoize f = memoize (f . eitherToBool) . boolToEither
    where boolToEither x = if x then Right () else Left ()
          eitherToBool = either (const False) (const True)

instance (Memoize a) => Memoize (Maybe a) where
  -- Maybe a <=> Either () a
  memoize f = memoize (f . eitherToMaybe) . maybeToEither
    where maybeToEither = maybe (Left ()) Right
          eitherToMaybe = either (const Nothing) Just

instance (Memoize a) => Memoize [a] where
  -- [a] <=> Maybe (a, [a])
  memoize f = memoize (f . maybeToList) . listToMaybe
    where
      listToMaybe :: [a] -> Maybe (a, [a])
      listToMaybe = uncons

      maybeToList :: Maybe (a, [a]) -> [a]
      maybeToList = maybe [] (uncurry (:))


-- numbers

-- Integer <=> (Bool, [Bool])
-- Where the first bool represents the sign bit and the list has all
-- the other bits

-- (well it's actually not quite a bijection because we could have -0
-- or extra leading 0s, but we won't in practice)

posToList :: Integer -> [Bool]
posToList 0 = []
posToList n = (n `mod` 2 == 1) : posToList (n `div` 2)

listToPos :: [Bool] -> Integer
listToPos [] = 0
listToPos (x:xs) = (if x then 1 else 0) + (listToPos xs * 2)

integerToList :: Integer -> (Bool, [Bool])
integerToList n = (n < 0, posToList (abs n))

listToInteger :: (Bool, [Bool]) -> Integer
listToInteger (neg, l) = (if neg then -1 else 1) * listToPos l

instance Memoize Integer where
  memoize f = memoize (f . listToInteger) . integerToList

instance Memoize Int where
  memoize f = memoize (f . fromInteger) . toInteger

instance Memoize Char where
  memoize f = memoize (f . toEnum) . fromEnum

-- It would be easy to add Word and all the different Ints
