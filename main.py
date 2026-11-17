
from dataclasses import dataclass
from drafter import *


# Site information appears on Drafter's built-in About page.
set_website_title("ActuaryHub")
set_site_information(
    author="CISC106 Student Project",
    description=(
        "An educational insurance policy manager that compares premiums "
        "with estimated expected claim costs."
    ),
    sources="Drafter documentation and CISC106 course materials.",
    planning="Project brainstorming and design documents are included in the repository.",
    links=[
        "https://github.com/clancysw/ActuaryHub",
        "https://clancysw.github.io/ActuaryHub/"
    ]
)
hide_debug_information()
set_website_framed(False)


@dataclass
class InsurancePolicy:
    """Store the financial and probability information for one policy."""

    name: str
    policy_type: str
    premium: float
    claim_probability: float
    claim_cost: float


@dataclass
class State:
    """Store saved policies and the current policy form information."""

    policies: list[InsurancePolicy]
    selected_policy: int
    policy_name: str
    policy_type: str
    premium: str
    claim_probability: str
    claim_cost: str
    message: str


def expected_loss(policy: InsurancePolicy) -> float:
    """Calculate the expected claim cost for one insurance policy.

    Args:
        policy: InsurancePolicy — policy whose probability and claim cost are used.

    Returns:
        float — the probability multiplied by the estimated claim cost.
    """
    return policy.claim_probability * policy.claim_cost


def money(amount: float) -> str:
    """Format a number as a dollar amount with two decimal places.

    Args:
        amount: float — numeric amount to format.

    Returns:
        str — the amount formatted as currency.
    """
    return "$" + format(amount, ",.2f")


def parse_policy_values(
    premium: str, claim_probability: str, claim_cost: str
) -> tuple[float, float, float] | None:
    """Convert form values to numbers and validate their allowed ranges.

    Args:
        premium: str — annual premium entered by the user.
        claim_probability: str — probability entered as a decimal from 0 to 1.
        claim_cost: str — estimated claim cost entered by the user.

    Returns:
        tuple[float, float, float] | None — validated values, or None if invalid.
    """
    try:
        premium_value = float(premium)
        probability_value = float(claim_probability)
        cost_value = float(claim_cost)
    except ValueError:
        return None

    if premium_value < 0 or cost_value < 0:
        return None
    if probability_value < 0 or probability_value > 1:
        return None

    return premium_value, probability_value, cost_value


def comparison_summary(policy: InsurancePolicy) -> str:
    """Explain how a policy's premium compares with its expected claim cost.

    Args:
        policy: InsurancePolicy — policy to evaluate.

    Returns:
        str — a sentence describing the comparison.
    """
    difference = policy.premium - expected_loss(policy)

    if difference > 0:
        return (
            "The premium is " + money(difference)
            + " above the expected claim cost."
        )
    if difference < 0:
        return (
            "The premium is " + money(abs(difference))
            + " below the expected claim cost."
        )
    return "The premium equals the expected claim cost."


def run_unit_tests() -> None:
    """Run assertions for calculation, formatting, validation, and comparison.

    Args:
        None.

    Returns:
        None — tests run through assertions; failures indicate a problem.
    """
    sample = InsurancePolicy("Test Auto", "Auto", 800, 0.15, 3000)
    assert expected_loss(sample) == 450
    assert money(450) == "$450.00"
    assert money(1200.5) == "$1,200.50"
    assert parse_policy_values("800", "0.15", "3000") == (
        800.0, 0.15, 3000.0
    )
    assert parse_policy_values("-1", "0.15", "3000") is None
    assert parse_policy_values("800", "1.5", "3000") is None
    assert parse_policy_values("abc", "0.15", "3000") is None
    assert comparison_summary(sample) == (
        "The premium is $350.00 above the expected claim cost."
    )


# These tests cover reusable calculation and validation functions.
# Routes are tested manually in the browser because they render Drafter
# pages and depend on navigation and form submissions.
run_unit_tests()
print("ACTUARYHUB IS RUNNING")


def navigation() -> list:
    """Build the navigation controls shared by every ActuaryHub page.

    Args:
        None.

    Returns:
        list — Drafter components for site navigation.
    """
    return [
        Header("ActuaryHub", 1),
        Paragraph("Your simple insurance risk explorer"),
        Button("Home", "home"),
        Button("Dashboard", "dashboard"),
        Button("Add Policy", "add_policy"),
        Button("Compare Policies", "compare_policies"),
        Button("About", "about"),
        HorizontalRule()
    ]


def make_page(state: State, content: list) -> Page:
    """Add shared navigation and the educational disclaimer to page content.

    Args:
        state: State — current website state.
        content: list — page-specific Drafter components.

    Returns:
        Page — the completed Drafter page.
    """
    content.append(HorizontalRule())
    content.append(SmallText(
        "Educational estimates only. Not an actual insurance quote."
    ))
    return Page(state, navigation() + content)


@route
def index(state: State) -> Page:
    """Route the default site address to the ActuaryHub homepage.

    Args:
        state: State — current website state.

    Returns:
        Page — the homepage returned by home.
    """
    return home(state)


@route
def home(state: State) -> Page:
    """Display the introduction and explain how to use ActuaryHub.

    Args:
        state: State — current website state.

    Returns:
        Page — the ActuaryHub homepage.
    """
    content = [
        Header("Welcome to ActuaryHub!", 2),
        Paragraph(
            "Create sample insurance policies and explore "
            "how probability affects expected claim costs."
        ),
        Header("How it works", 3),
        Paragraph("1. Create an insurance policy."),
        Paragraph("2. Enter its premium and estimated claim information."),
        Paragraph("3. Calculate its expected claim cost."),
        Paragraph("4. Compare it with other policies."),
        Button("Open Dashboard", "dashboard"),
        Button("Create a Policy", "add_policy")
    ]
    return make_page(state, content)


@route
def dashboard(state: State) -> Page:
    """Show saved policies and provide links to their detail pages.

    Args:
        state: State — current website state containing saved policies.

    Returns:
        Page — the policy dashboard.
    """
    content = [
        Header("Policy Dashboard", 2),
        Paragraph("Policies saved: " + str(len(state.policies)))
    ]

    if len(state.policies) == 0:
        content.append(Paragraph("You have not created any policies yet."))
        content.append(Button("Add Your First Policy", "add_policy"))
    else:
        for index, policy in enumerate(state.policies):
            content.append(Header(policy.name, 3))
            content.append(Paragraph("Type: " + policy.policy_type))
            content.append(Paragraph("Premium: " + money(policy.premium)))
            content.append(Paragraph(
                "Expected claim cost: " + money(expected_loss(policy))
            ))
            content.append(Button(
                "View Details",
                "policy_details",
                {"index": index}
            ))

    if state.message:
        content.append(Paragraph(state.message))

    return make_page(state, content)


@route
def add_policy(state: State) -> Page:
    """Display the form for creating a new insurance policy.

    Args:
        state: State — current website state and form values.

    Returns:
        Page — the new-policy form.
    """
    content = [
        Header("Create an Insurance Policy", 2),
        Paragraph("Enter the information for your new policy."),
        "Policy name",
        TextBox("policy_name", state.policy_name),
        "Policy type",
        TextBox("policy_type", state.policy_type),
        "Annual premium ($)",
        TextBox("premium", state.premium),
        "Claim probability (0 to 1)",
        TextBox("claim_probability", state.claim_probability),
        "Estimated claim cost ($)",
        TextBox("claim_cost", state.claim_cost),
        Button("Save Policy", "save_policy")
    ]

    if state.message:
        content.append(Paragraph(state.message))

    return make_page(state, content)


@route
def save_policy(
    state: State,
    policy_name: str,
    policy_type: str,
    premium: str,
    claim_probability: str,
    claim_cost: str
) -> Page:
    """Validate submitted form values and add a new policy to the saved list.

    Args:
        state: State — current website state to update.
        policy_name: str — name entered for the policy.
        policy_type: str — category entered for the policy.
        premium: str — annual premium entered by the user.
        claim_probability: str — claim probability entered as a decimal.
        claim_cost: str — estimated claim cost entered by the user.

    Returns:
        Page — policy details after saving, or the form with an error message.
    """
    state.policy_name = policy_name
    state.policy_type = policy_type
    state.premium = premium
    state.claim_probability = claim_probability
    state.claim_cost = claim_cost

    if not policy_name.strip() or not policy_type.strip():
        state.message = "Please enter both a policy name and a policy type."
        return add_policy(state)

    values = parse_policy_values(premium, claim_probability, claim_cost)
    if values is None:
        state.message = (
            "Check your numbers: premium and claim cost must be nonnegative, "
            "and probability must be between 0 and 1."
        )
        return add_policy(state)

    premium_value, probability_value, cost_value = values
    new_policy = InsurancePolicy(
        policy_name.strip(),
        policy_type.strip(),
        premium_value,
        probability_value,
        cost_value
    )

    state.policies.append(new_policy)
    state.selected_policy = len(state.policies) - 1
    state.message = "Success: your policy was created and saved."
    state.policy_name = ""
    state.policy_type = ""
    state.premium = ""
    state.claim_probability = ""
    state.claim_cost = ""

    return policy_details(state, state.selected_policy)


@route
def policy_details(state: State, index: int) -> Page:
    """Display a selected policy's information and expected claim cost.

    Args:
        state: State — current website state.
        index: int — zero-based position of the policy in state.policies.

    Returns:
        Page — policy details, or the dashboard if the index is invalid.
    """
    if index < 0 or index >= len(state.policies):
        state.message = "That policy could not be found. Return to the dashboard."
        return dashboard(state)

    state.selected_policy = index
    policy = state.policies[index]
    loss = expected_loss(policy)
    content = [
        Header(policy.name, 2),
        Paragraph("Policy type: " + policy.policy_type),
        Paragraph("Annual premium: " + money(policy.premium)),
        Paragraph("Claim probability: " + str(policy.claim_probability)),
        Paragraph("Estimated claim cost: " + money(policy.claim_cost)),
        Header("Expected Claim Cost", 3),
        Paragraph(money(loss)),
        Paragraph(comparison_summary(policy))
    ]

    if state.message:
        content.append(Paragraph(state.message))
        state.message = ""

    content.append(Button(
        "Edit Policy", "edit_policy", {"index": index}
    ))
    content.append(Button("Back to Dashboard", "dashboard"))
    return make_page(state, content)


@route
def edit_policy(state: State, index: int) -> Page:
    """Display an existing policy in an editable form.

    Args:
        state: State — current website state.
        index: int — zero-based position of the policy to edit.

    Returns:
        Page — the edit form, or the dashboard if the index is invalid.
    """
    if index < 0 or index >= len(state.policies):
        state.message = "That policy could not be found. Return to the dashboard."
        return dashboard(state)

    policy = state.policies[index]
    state.selected_policy = index

    # Keep attempted form values visible after a validation error.
    if state.message:
        name_value = state.policy_name
        type_value = state.policy_type
        premium_value = state.premium
        probability_value = state.claim_probability
        cost_value = state.claim_cost
    else:
        name_value = policy.name
        type_value = policy.policy_type
        premium_value = str(policy.premium)
        probability_value = str(policy.claim_probability)
        cost_value = str(policy.claim_cost)

    content = [
        Header("Edit Policy", 2),
        "Policy name",
        TextBox("policy_name", name_value),
        "Policy type",
        TextBox("policy_type", type_value),
        "Annual premium ($)",
        TextBox("premium", premium_value),
        "Claim probability (0 to 1)",
        TextBox("claim_probability", probability_value),
        "Estimated claim cost ($)",
        TextBox("claim_cost", cost_value),
        Button("Save Changes", "update_policy"),
        Button("Cancel", "policy_details", {"index": index})
    ]

    if state.message:
        content.append(Paragraph(state.message))

    return make_page(state, content)


@route
def update_policy(
    state: State,
    policy_name: str,
    policy_type: str,
    premium: str,
    claim_probability: str,
    claim_cost: str
) -> Page:
    """Validate edited values and replace the selected saved policy.

    Args:
        state: State — current website state to update.
        policy_name: str — updated policy name.
        policy_type: str — updated policy category.
        premium: str — updated annual premium.
        claim_probability: str — updated claim probability as a decimal.
        claim_cost: str — updated estimated claim cost.

    Returns:
        Page — updated details, or the edit form/dashboard if validation fails.
    """
    state.policy_name = policy_name
    state.policy_type = policy_type
    state.premium = premium
    state.claim_probability = claim_probability
    state.claim_cost = claim_cost

    if not policy_name.strip() or not policy_type.strip():
        state.message = "Please enter both a policy name and a policy type."
        return edit_policy(state, state.selected_policy)

    values = parse_policy_values(premium, claim_probability, claim_cost)
    if values is None:
        state.message = (
            "Check your numbers: premium and claim cost must be nonnegative, "
            "and probability must be between 0 and 1."
        )
        return edit_policy(state, state.selected_policy)

    index = state.selected_policy
    if index < 0 or index >= len(state.policies):
        state.message = "That policy could not be found. Return to the dashboard."
        return dashboard(state)

    premium_value, probability_value, cost_value = values
    state.policies[index] = InsurancePolicy(
        policy_name.strip(),
        policy_type.strip(),
        premium_value,
        probability_value,
        cost_value
    )

    state.message = "Success: your policy changes were saved."
    state.policy_name = ""
    state.policy_type = ""
    state.premium = ""
    state.claim_probability = ""
    state.claim_cost = ""
    return policy_details(state, index)


@route
def compare_policies(state: State) -> Page:
    """Compare each saved policy's premium with its expected claim cost.

    Args:
        state: State — current website state containing policies to compare.

    Returns:
        Page — comparison results or a message when no policies exist.
    """
    content = [
        Header("Compare Policies", 2),
        Paragraph(
            "Compare each policy's premium against its expected claim cost. "
            "A positive difference means the premium is above expected cost; "
            "a negative difference means it is below expected cost."
        )
    ]

    if len(state.policies) == 0:
        content.append(Paragraph("There are no policies to compare yet."))
        content.append(Button("Add a Policy", "add_policy"))
    else:
        for policy in state.policies:
            loss = expected_loss(policy)
            difference = policy.premium - loss
            content.append(Header(policy.name, 3))
            content.append(Paragraph(
                "Annual premium: " + money(policy.premium)
            ))
            content.append(Paragraph(
                "Expected claim cost: " + money(loss)
            ))
            content.append(Paragraph(
                "Premium minus expected claim cost: " + money(difference)
            ))
            content.append(Paragraph(comparison_summary(policy)))

    return make_page(state, content)


@route
def about(state: State) -> Page:
    """Explain ActuaryHub's educational purpose and expected claim cost formula.

    Args:
        state: State — current website state.

    Returns:
        Page — the About page.
    """
    content = [
        Header("About ActuaryHub", 2),
        Paragraph(
            "ActuaryHub is an educational project about insurance "
            "risk and expected value."
        ),
        Header("The Formula", 3),
        Paragraph(
            "Expected claim cost = Claim probability x Estimated claim cost"
        ),
        Header("Example", 3),
        Paragraph(
            "A 20% probability of a $5,000 claim produces "
            "an expected claim cost of $1,000."
        ),
        Paragraph(
            "Real insurance pricing uses many additional factors. "
            "This project is a simplified educational model."
        ),
        Button("Return Home", "home")
    ]
    return make_page(state, content)


# Start the website with two sample policies.
start_server(State(
    policies=[
        InsurancePolicy("Sample Auto", "Auto", 1200, 0.12, 6000),
        InsurancePolicy("Sample Home", "Home", 900, 0.08, 9000)
    ],
    selected_policy=-1,
    policy_name="",
    policy_type="",
    premium="",
    claim_probability="",
    claim_cost="",
    message="Welcome to ActuaryHub!"
))
