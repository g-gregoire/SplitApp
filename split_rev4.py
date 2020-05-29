### Splitting Program 
### by Georges Gregoire
### Rev. 4
### Revision Start Date: 2018-10-09
### Last Reivision Date: 
### Revision Notes: added function Add() which makes adding users look cleaner
### added directional payment, so system tells people who they need to pay

# class App(object):
# 	"""General App class"""
# 	def __init__(self, arg):
# 		super(App, self).__init__()
# 		self.List = []

# 	def group(Name, Description):
		
class User(object):
	"""User class for holding dictionaries for Split users"""
	def __init__(self, name):
		#super(ClassName, self).__init__()
		self.name = name
		self.items = []

	#items= []
	total_buy= 0.00
	total_net=0.00
	net_payment=0.00

	def buy(self, value, splitValue):
		self.total_buy += value
		self.total_net += splitValue
		self.net_payment += splitValue
		self.items.append(value)

	def owe(self, value):
		self.total_net -= value
		self.net_payment -= value

	def info(self):
		print("----------------")
		if len(self.items) > 0:
			print("%s payed for a total of $%.2f." %(self.name, self.total_buy))
		else:
			pass
			#print("%s didn't buy anything." %(self.name))
		if self.total_net > 0:
			print("%s gets back $%.2f." %(self.name, self.total_net))
		elif self.total_net < 0:
			print("%s owes $%.2f." %(self.name, -1 * self.total_net))
		else:
			print("%s owes Nothing!" %(self.name))


class Group(object):
	def __init__(self, GroupName, Description):
		self.name = GroupName
		self.desc = Description
		self.team = {"names" : [], "payment": [], "transfer": [], "pay_to": [], "net_due": [], "payed_for": [], "total": 0,}
		self.Users = []

	def addUser(self, UserName):
		self.team["names"].append(UserName)
		self.team["payment"].append(0.00)
		self.team["transfer"].append(0.00)
		self.team["net_due"].append(0.00)
		self.team["payed_for"].append(0.00)
		self.team["pay_to"].append(-1)
		self.Users.append(User(UserName))
		self.team["total"] += 1
		#print("Added %s to the adventure!" %(UserName))
		print("Added %s!" %(UserName))
		
	def info(self):
		total = group1.team["total"]

		for index in range(total):
			names = group1.team["names"][index]
			transfer = group1.team["transfer"][index]
			net_due = group1.team["net_due"][index]
			payed_for = group1.team["payed_for"][index]
			pay_to = group1.team["pay_to"][index]
			print("----------------")
			if payed_for != 0:
				print("%s payed for a total of $%.2f." %(names, payed_for))
			else:
				pass
				#print("%s didn't buy anything." %(names))
			
			if net_due > 0.01:
				print("%s gets $%.2f back in total." %(names, net_due))
			elif net_due < 0.01:
				print("%s owes $%.2f in total." %(names, -1 * net_due))
			else:
				print("%s owes Nothing!" %(names))

			if pay_to == -1:
				print("%s owes Nothing!" %(names))
			elif transfer > 0.01:
				print("%s gets $%.2f from %s." %(names, transfer, group1.team["names"][pay_to]))
			elif transfer < -0.01:
				print("%s pay %s $%.2f." %(names, group1.team["names"][pay_to], -1 * transfer))
			else:
				print("%s owes Nothing!" %(names))



def Info(Name):
	index=group1.team["names"].index(Name)
	group1.Users[index].info()

def Add(Name):
	group1.addUser(Name)

def Purchase(Name_me, Price, Scope, buyerPays = 1):
	index_me=group1.team["names"].index(Name_me) #Gets index number of buyer
	if Scope == "All" or Scope == "all":
		if buyerPays == 1: #If buyer does not "own" item (bP=0), reduce group size by one
			SplitPrice = Price/group1.team["total"] #Calculate per-person cost
			group1.Users[index_me].buy(Price, Price - SplitPrice)
			addDues(Price, index_me, Price - SplitPrice)
		else:
			SplitPrice = Price/(group1.team["total"] - 1) #Calculate per-person cost without buyer included
			group1.Users[index_me].buy(Price, Price)
			addDues(Price, index_me, Price)
		for name in group1.team["names"]:
			index=group1.team["names"].index(name)
			group1.Users[index].owe(SplitPrice)
			addDues(0, index, SplitPrice, -1)

		group1.Users[index_me].owe(SplitPrice*-1) #Used so that buyer is not charged for his own purchase
		addDues(0, index_me, SplitPrice)
	
	else:
		length =  len(Scope) 
		if buyerPays == 1:
			 SplitPrice = Price/(length + 1) #Add one to account for person who actually payed for it
			 group1.Users[index_me].buy(Price, Price - SplitPrice)
			 addDues(Price, index_me, Price - SplitPrice)
		else: 
			SplitPrice = Price/length#Don't add because buyer doesn't "own" this item
			group1.Users[index_me].buy(Price, Price)
			addDues(Price, index_me, Price)

		for name in Scope:
			index=group1.team["names"].index(name)
			group1.Users[index].owe(SplitPrice)
			addDues(0, index, SplitPrice, -1)
			
def Split():
	# for name in group1.team["names"]:
	# 	Info(name)
	payment = group1.team["payment"] #Amount that needs to reach 0
	transfer = group1.team["transfer"] #What is being transfered to someone else
	net_due = group1.team["net_due"] #Overall amount that each person owes or is owed
	# print("Net Due:", net_due)
	pay2 = group1.team["pay_to"]
	# print("Before:")
	# print(payment)
	# print("After Split:")

	for dues in payment:
		maxIndex = payment.index(max(payment))
		if dues < 0:
			index=group1.team["payment"].index(dues)
			payment[maxIndex] += dues
			transfer[maxIndex] += dues
			payment[index] = 0.00
			pay2[index] = maxIndex
			# print("Payment ",payment)
			# print("Transfer1 ",transfer)
			# print(pay2)
			# print("Net Due:", net_due)

	while abs(max(payment)) > 0.01:
		for dues in payment:
			if dues < 0:
				maxIndex = payment.index(max(payment))
				index=group1.team["payment"].index(dues)
				payment[maxIndex] += dues
				transfer[maxIndex] += dues
				payment[index] = 0.00
				pay2[index] = maxIndex
				# print("Net ", payment)
				# print("Transfer ", transfer)
				# print(pay2)
		# print(payment)

	# print("Net Due:", net_due)
	# print("Payed for", group1.team["payed_for"])
	group1.info()

def addDues(price, index, amount, sign = 1):
	group1.team["payment"][index] += sign * amount
	group1.team["transfer"][index] += sign * amount
	group1.team["net_due"][index] += sign * amount
	group1.team["payed_for"][index] += price


#--- USE BELOW TO CREATE YOUR GROUP AND ADD USERS ---#
# - Create Group here
group1 = Group("Camping Trip", "Trip to Algonquin 2018")

# - Add Users here
Add("Owen")
Add("Stew")
Add("Nikhil")
Add("Georges")
Add("Lexi")
Add("Derek")
Add("Monica")
Add("Ben")
Add("Peter")
Add("Alex")
Add("Shannon")
Add("Mcfadden")
# - Add Purchases here. NOTE: IF SPECIFYING NAMES, DON'T INCLUDE BUYER, THIS IS ACCOUNTED FOR ALREADY
# Note: set buyerPays to 0 if buyer paid for something that was not for him.
Purchase("Georges", 275, "All") 
Purchase("Georges", 9, ["Shannon"], 0) 
Purchase("Georges", 18, ["Lexi"], 0) 
Purchase("Georges", 16, ["Ben"], 0) 
Purchase("Peter", 70, "All") 

# - Print out everyone's dues
Split()

			