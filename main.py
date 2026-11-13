from dataclasses import dataclass
from drafter import *

print("ACTUARYHUB IS RUNNING")

@dataclass
class InsurancePolicy:
    name: str
    policy_type: str
    premium: float
    claim_probability: float
    claim_cost: float


@dataclass
class State:
    policies: list[InsurancePolicy]
    selected_policy: int
    policy_name: str
    policy_type: str
    premium: str
    claim_probability: str
    claim_cost: str
    message: str


def expected_loss(policy: InsurancePolicy) -> float:
    return policy.claim_probability * policy.claim_cost


def money(amount: float) -> str:
    return "$" + format(amount, ",.2f")


def navigation() -> list:
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
    content.append(HorizontalRule())
    content.append(SmallText(
        "Educational estimates only. Not an actual insurance quote."
    ))
    return Page(state, navigation() + content)

@route
def index(state: State) -> Page:
    return home(state)

@route
def home(state: State) -> Page:
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
                "Expected loss: " + money(expected_loss(policy))
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

    state.policy_name = policy_name
    state.policy_type = policy_type
    state.premium = premium
    state.claim_probability = claim_probability
    state.claim_cost = claim_cost

    if not policy_name.strip() or not policy_type.strip():
        state.message = "Please enter a policy name and type."
        return add_policy(state)

    try:
        premium_value = float(premium)
        probability_value = float(claim_probability)
        cost_value = float(claim_cost)
    except ValueError:
        state.message = "Please enter valid numbers in all three number fields."
        return add_policy(state)

    if premium_value < 0 or cost_value < 0:
        state.message = "Premium and claim cost cannot be negative."
        return add_policy(state)

    if probability_value < 0 or probability_value > 1:
        state.message = "Probability must be between 0 and 1."
        return add_policy(state)

    new_policy = InsurancePolicy(
        policy_name.strip(),
        policy_type.strip(),
        premium_value,
        probability_value,
        cost_value
    )

    state.policies.append(new_policy)
    state.selected_policy = len(state.policies) - 1
    state.message = "Policy successfully created!"

    state.policy_name = ""
    state.policy_type = ""
    state.premium = ""
    state.claim_probability = ""
    state.claim_cost = ""

    return policy_details(state, state.selected_policy)


@route
def policy_details(state: State, index: int) -> Page:
    if index < 0 or index >= len(state.policies):
        state.message = "Policy not found."
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
        Paragraph(money(loss))
    ]

    if policy.premium >= loss:
        content.append(Paragraph(
            "The premium is " + money(policy.premium - loss)
            + " higher than the expected claim cost."
        ))
    else:
        content.append(Paragraph(
            "The expected claim cost is "
            + money(loss - policy.premium)
            + " higher than the premium."
        ))

    content.append(Button(
        "Edit Policy", "edit_policy", {"index": index}
    ))
    content.append(Button("Back to Dashboard", "dashboard"))

    return make_page(state, content)


@route
def edit_policy(state: State, index: int) -> Page:
    if index < 0 or index >= len(state.policies):
        state.message = "Policy not found."
        return dashboard(state)

    policy = state.policies[index]
    state.selected_policy = index

    content = [
        Header("Edit Policy", 2),
        "Policy name",
        TextBox("policy_name", policy.name),
        "Policy type",
        TextBox("policy_type", policy.policy_type),
        "Annual premium ($)",
        TextBox("premium", str(policy.premium)),
        "Claim probability (0 to 1)",
        TextBox("claim_probability", str(policy.claim_probability)),
        "Estimated claim cost ($)",
        TextBox("claim_cost", str(policy.claim_cost)),
        Button("Save Changes", "update_policy"),
        Button("Cancel", "policy_details", {"index": index})
    ]

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

    if not policy_name.strip() or not policy_type.strip():
        state.message = "Please enter a policy name and type."
        return edit_policy(state, state.selected_policy)

    try:
        premium_value = float(premium)
        probability_value = float(claim_probability)
        cost_value = float(claim_cost)
    except ValueError:
        state.message = "Please enter valid numbers."
        return edit_policy(state, state.selected_policy)

    if premium_value < 0 or cost_value < 0:
        state.message = "Premium and claim cost cannot be negative."
        return edit_policy(state, state.selected_policy)

    if probability_value < 0 or probability_value > 1:
        state.message = "Probability must be between 0 and 1."
        return edit_policy(state, state.selected_policy)

    index = state.selected_policy

    if index < 0 or index >= len(state.policies):
        state.message = "Policy not found."
        return dashboard(state)

    state.policies[index] = InsurancePolicy(
        policy_name.strip(),
        policy_type.strip(),
        premium_value,
        probability_value,
        cost_value
    )

    state.message = "Policy successfully updated!"
    return policy_details(state, index)


@route
def compare_policies(state: State) -> Page:
    content = [
        Header("Compare Policies", 2),
        Paragraph(
            "Compare each policy's premium against its expected claim cost."
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
                "Premium: " + money(policy.premium)
            ))
            content.append(Paragraph(
                "Expected claim cost: " + money(loss)
            ))
            content.append(Paragraph(
                "Premium minus expected loss: " + money(difference)
            ))

    return make_page(state, content)


@route
def about(state: State) -> Page:
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
