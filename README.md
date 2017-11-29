# Manipulator trajectory generator
This Python script computes the coefficients of any polynomial trajectories.

### Usage
First install `python`, `numpy` and `matplotlib`.

Run command `python main.py *[paramters]*`

The `*[paramters]*` should be separated by spaces and includes:
- `method`: The order of polynomials. E.g. For 4-3-4, use `4 3 4`
- `init`: The initial (angular) velocity and acceleration. E.g. `0 5`. If any of the two is unspecified, use colon (`:`). E.g. `0 :` means an initial velocity of 0 and initial acceleration is unspecified. It's important to make sure the number of unknowns is equal to the number of equations. E.g. if the method is `3 3 3 3 3`, the number of unknown coefficients is `(3+1)*5=20` while each specified angles and continuous velocity and acceleration requirements gives `18` equations for those 6 points where the trajectory goes through. Therefore, only `20-18=2` numbers can be specified in `init` and `final` combined to make sure the equation has unique solution.
- `final`: Similar to `init` but for the final velocity and accleration.
- `times` and `angles`: If we want the angles to be at 0, 20, 40, and 60 at time 0, 1, 2, and 3 respectively, `times` should be `0 1 2 3` and `angles` should be `0 20 40 60`.

Type the the above parameters in the order above. A correct command looks like `python main.py 4 3 4 0 0 0 0 0 1 2 3 0 20 40 60`.

The computed polynomials will be shown on stdout. An x-t diagram will be shown.

### License
This script is dedicated to public domain.
