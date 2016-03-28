from vedic import VedicNumber


def construct_steps(x, y, max_len):
	# Number of steps will be 2 * num_digits - 1
	num_steps = (2 * max_len) - 1
	steps = dict()

	# Steps are symmetrical on either side of halfway mark
	for idx in range(0, (num_steps >> 1) + 1):
		lhs_x_operands = list()
		lhs_y_operands = list()
		rhs_x_operands = list()
		rhs_y_operands = list()

		for i in range(0, idx + 1):
			lhs_x_operands.append(x[max_len - 1 - i])
			lhs_y_operands.append(y[max_len - 1 - i])
			rhs_x_operands.append(x[i])
			rhs_y_operands.append(y[i])
		steps[idx + 1] = (lhs_x_operands, lhs_y_operands)
		steps[num_steps - idx] = (rhs_x_operands, rhs_y_operands)
	sorted_keys = sorted(steps.keys(), reverse=True)
	# Return an array of num1, num2 tuples
	return [steps[key] for key in sorted_keys]


def execute_steps(steps):
	execution_stack = []

	for tup in steps:
		# First tuple is num1 ops and second is num2 ops
		all_zeroes = all([tup[0][i] == '0' for i in range(0, len(tup[0]))]) or all(
			[tup[1][i] == '0' for i in range(0, len(tup[1]))])
		if all_zeroes:
			# print('All zeroes ', all_zeroes)
			exec_result = '0'
		if all_zeroes is False:
			exec_result = sum([int(tup[0][i]) * int(tup[1][len(tup[0]) - 1 - i]) for i in range(0, len(tup[0]))])
			execution_stack.append(str(exec_result))
	# print(execution_stack)
	return execution_stack


def combine(execution_stack):
	# Final output stack
	result_stack = []
	carry = 0

	while len(execution_stack) > 0:
		top = execution_stack.pop()
		# Add carry to it if present
		top = str(int(top) + int(carry))
		# Reset carry
		carry = 0
		if len(top) > 1:
			result_stack.append(top[-1])
			# Push other part to carry
			carry = top[:-1]
		else:
			result_stack.append(top)
	# If any carry remains we need to push that as well
	if carry != 0:
		result_stack.append(carry)
	output = []
	found_consequent_digit = False

	while len(result_stack) > 0:
		top = result_stack.pop()
		# Do not append inconsequential zeroes
		if int(top) > 0:
			found_consequent_digit = True
		if found_consequent_digit:
			output.append(top)
	return VedicNumber("".join(output))
