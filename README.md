# nursery
RobotVera interview case

API endpoints:
## Kids at `/kids/`
Methods:
  * `get`: get all kids
  * `post`: add new kid from POST arguments
  
## Kids at `/kids/<int:kid_id>/`
Methods:
  * `get`: get single kid
  * `post`: update kid
  
## Journal at `/journal/`:
Methods:
  * `get`: get all kids currently studying in nursery
## Journal at `/journal/<int:kid_id>/`
Methods:
  * `get`: get last kid related entries
  * `post`: add entry. POST should have relative argument as 'F' or 'M'
  
  
