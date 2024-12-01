SELECT id,
  username,
  password
FROM users
WHERE username = %s;