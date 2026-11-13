# ActuaryHub

ActuaryHub is an educational insurance policy manager built with Python and
Drafter. It lets a visitor add, view, edit, and compare sample insurance
policies using a simplified expected-claim-cost calculation.

## Calculation

`Expected claim cost = claim probability × estimated claim cost`

Enter claim probability as a decimal from `0` to `1` (for example, `0.15` for
15%). This project is an educational demonstration, not an insurance quote or
professional financial advice.

## Files

* `main.py` — Drafter website, dataclasses, routes, validation, and checks.
* `requirements.txt` — Python dependency list.
* `README.md` — project and setup instructions.

## Run locally in Thonny

1. Install Drafter in the Python environment used by Thonny:

```bash
   python -m pip install drafter
   ```

2. Open `main.py` in Thonny.
3. Run the file. Drafter should open the website in your browser.
4. Try adding a policy, viewing it, editing it, and comparing policies.

The current Drafter state is held in the browser's memory. Reloading the page
restarts the app and clears the sample policies; this version does not use a
database or persistent storage.

## Deploy

Follow the course's Drafter GitHub Pages deployment instructions:

https://drafter-edu.github.io/drafter/your-project/deploy/github-pages/

Make the repository public, include all project files and required worksheets,
run the deployment process, and test the published URL. If you change the code
after deployment, deploy again.

## Rubric checklist

* 9 application routes: `home`, `dashboard`, `add\_policy`, `save\_policy`,
`policy\_details`, `edit\_policy`, `update\_policy`, `compare\_policies`, `about`.
* 7 pages/screens: home, dashboard, add policy, policy details, edit policy,
compare policies, and about.
* Two dataclasses: `State` and `InsurancePolicy`.
* State stores a list of `InsurancePolicy` instances and form/selection/message
values that are changed by routes.
* Five text-box inputs on the add/edit forms.
* Multiple meaningful conditionals for validation, empty lists, index checks,
and comparison feedback.
* Loops iterate through the list of `InsurancePolicy` objects on the dashboard
and comparison page.
* Basic assertions check expected-loss math, currency formatting, and input
validation.

## Important course submission note

Include your actual LLM conversation transcript and the required brainstorming
and design worksheets in the repository. Do not label reconstructed or mock
conversations as verbatim transcripts.

