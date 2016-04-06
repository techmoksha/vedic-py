from itertools import chain


class VedicNumber:

	def __init__(self, num):
		if isinstance(num, int):
			num = str(num)
		self.num = num

	def __add__(self, other):
		return Ops.add([self, other])

	def __mul__(self, other):
		return Ops.multiply(self, other)

	def __sub__(self, other):
		return Ops.subtract(self, other)

	def __str__(self):
		return self.num


class Ops(object):

	@staticmethod
	def leftpad_zeroes(string, num):
		"""
		Left pad a string with number of 0s = num
		:param string: String to pad
		:param num: Number of 0s to prepend
		:return:
		"""
		output = ['0' for i in range(0, num)]
		output = "".join(output)
		return output + string

	@staticmethod
	def rightpad_zeroes(string, num):
		"""
		Right pad a string with number of 0s = num
		:param string: String to pad
		:param num: Number of 0s to append
		:return:
		"""
		output = ['0' for i in range(0, num)]
		output = "".join(output)
		return string + output

	@staticmethod
	# TODO handle negative numbers
	def add(nums):
		"""
		Performs addition of all numbers based on vedic addition sutra
		:param nums : Array of numbers to be added. Each number can be string or int or #VedicNumber
		:return: Result of addition as a #VedicNumber
		"""
		# Get digits in number Convert to string
		nums = list(map(lambda num: str(num) if isinstance(num, VedicNumber) or isinstance(num, int) else num, nums))
		# Get length of biggest number
		max_len = max([len(num) for num in nums])
		# Left pad where required
		nums = list(map(lambda num: Ops.leftpad_zeroes(num, max_len - len(num)), nums))

		# First one is added by default since at least one digit will be present
		part1 = str(sum([int(num[0]) for num in nums]))
		main_stack = list()
		# Append every character separately
		[main_stack.append(s) for s in part1]

		for idx in range(1, max_len):
			# Add x[0] with y[0], x[1] with y[1] and so on while combining
			part2 = sum([int(num[idx]) for num in nums])
			# Convert back to string
			part2 = str(part2)
			if len(part2) == 1:
				# Append it to part 1 (Combine op)
				main_stack.append(part2)
			else:
				# Add result to last digit of part 1 with carry from part2(Combine op)
				res = part2
				residual_stack = list()
				if len(res) == 1:
					residual_stack.append(part2[-1])
				# Till res is a single digit we need to recurse
				while len(res) > 1:
					part1 = main_stack.pop()
					res = str(int(part1) + int(part2[0]))
					residual_stack.append(part2[-1])
					if len(res) > 1:
						part2 = res
				main_stack.append(str(res))
				# Append residual stack
				main_stack = list(chain(main_stack, residual_stack))
				residual_stack = None
		return VedicNumber("".join(main_stack))

	@staticmethod
	def subtract(x, y):
		"""
		Performs subtraction of y from x based on vedic subtraction sutra
		:param x : Larger number. Can be string or int or #VedicNumber
		:param y : Smaller number. Can be string or int or #VedicNumber
		:return: Result of subtraction as #VedicNumber
		"""
		if isinstance(x, int) or isinstance(x, VedicNumber):
			x = str(x)
		if isinstance(y, int) or isinstance(y, VedicNumber):
			y = str(y)
		max_len = max(len(x), len(y))
		x = Ops.leftpad_zeroes(x, max_len - len(x))
		y = Ops.leftpad_zeroes(y, max_len - len(y))

		main_stack = list()
		found_conseq_digit = False
		inconseq_zeroes = 0
		main_stack.append(str(int(x[0]) - int(y[0])))

		for idx in range(1, max_len):
			num1 = int(x[idx])
			num2 = int(y[idx])

			if num1 < num2:
				# Pop off the earlier number
				top = main_stack.pop()
				# Reduce the previous number
				top = int(top) - 1
				main_stack.append(str(top))
				correction_stack = list()

				while top < 0:
					# Need to apply correction by adding negative number to 10
					# Pop off the top element and reduce by 1
					top = main_stack.pop()
					correction = 10 + int(top)
					# Since correction is applied, 1 has to be deducted from new top
					top = main_stack.pop()
					top = int(top) - 1
					main_stack.append(str(top))
					correction_stack.append(str(correction))
				main_stack = list(chain(main_stack, correction_stack))
				correction_stack = None
				# Add 10 to num1
				num1 += 10
			if found_conseq_digit is not True:
				# Check top element
				top_most = main_stack[-1]
				if top_most == '0':
					inconseq_zeroes += 1
				else:
					found_conseq_digit = True
			main_stack.append(str(num1 - num2))
		return VedicNumber("".join(main_stack[inconseq_zeroes:]))

	@staticmethod
	def multiply(x, y):
		"""
		Performs multiplication of x and y based on vedic general multiplication sutra
		:param x : Can be string int or #VedicNumber
		:param y : Can be string int or #VedicNumber
		:return: Result of multiplication as #VedicNumber
		"""
		if isinstance(x, int) or isinstance(x, VedicNumber):
			x = str(x)
		if isinstance(y, int) or isinstance(y, VedicNumber):
			y = str(y)
		max_len = max(len(x), len(y))
		x = Ops.leftpad_zeroes(x, max_len - len(x))
		y = Ops.leftpad_zeroes(y, max_len - len(y))

		# Results of individual cross multiples
		execution_dict = Ops.perform_mult(x, y, max_len)
		# Reduce to get final result
		return Ops.reduce(execution_dict)

	@staticmethod
	def perform_mult(x, y, max_len):
		# Number of steps will be 2 * num_digits - 1
		num_steps = (2 * max_len) - 1
		execution_dict = dict()

		# Steps are symmetrical on either side of halfway mark
		for idx in range(0, (num_steps >> 1) + 1):
			exec_result_lhs = 0
			exec_result_rhs = 0
			for i in range(0, idx + 1):
				exec_result_lhs += int(x[max_len - 1 - i]) * int(y[max_len - 1 - idx + i])
				exec_result_rhs += int(x[i]) * int(y[idx - i])
			execution_dict[idx + 1] = exec_result_lhs
			execution_dict[num_steps - idx] = exec_result_rhs

		return execution_dict

	@staticmethod
	def reduce(execution_dict):
		# print(execution_dict)
		# Final output stack
		result_stack = []
		carry = 0

		keys = execution_dict.keys()
		for i in range(1, len(keys) + 1):
			top = execution_dict[i]
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

	@staticmethod
	def fact(num):
		result = VedicNumber(2)
		for i in range(3, num + 1):
			result *= VedicNumber(i)
		return result
