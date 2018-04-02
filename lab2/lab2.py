from munkres import Munkres, print_matrix, make_cost_matrix
import numpy as np


DATA_FILE_NAME = 'data'


def read_data():
	m, n, specialists_count_by_group, workplaces_count, specialist_performance_by_group = 0, 0, [], [], []
	with open(DATA_FILE_NAME) as data:
		m, n = [int(x) for x in data.readline().split()]
		print 'm: ' + str(m) + ', n: ' + str(n)		
		specialists_count_by_group = [int(x) for x in data.readline().split()]
		print 'specialists_count_by_group: ' + str(specialists_count_by_group)
		workplaces_count = [int(x) for x in data.readline().split()]
		print 'workplaces_count: ' + str(workplaces_count)
		for i in range(m):
			i_specialist_group_performance = [float(x) for x in data.readline().split()]
			specialist_performance_by_group.append(i_specialist_group_performance)
		print 'specialist_performance_by_group:'
		print specialist_performance_by_group
		print

	return m, n, specialists_count_by_group, workplaces_count, specialist_performance_by_group


def make_performance_matrix(m, n, specialists_count_by_group, workplaces_count, specialist_performance_by_group):
	total_specialists_count = sum(specialists_count_by_group)
	matrix = np.zeros((total_specialists_count, total_specialists_count))
	curr_row = 0
	# iterating every specialist group from A[0] to A[m-1]
	for i in range(m):
		specialists_count_in_group = specialists_count_by_group[i]
		# iterating every specialist in the group
		for k in range(specialists_count_in_group):
			curr_column = 0
			# iterating every work type
			for j in range(n):
				workplaces_count_for_work = workplaces_count[j]
				# iterating every workplace for the work type
				for l in range(workplaces_count_for_work):
					matrix[curr_row + k][curr_column + l] = specialist_performance_by_group[i][j]
				curr_column += workplaces_count_for_work
		curr_row += specialists_count_in_group
	print 'performance matrix:'
	print matrix
	print

	return matrix


def munkres(n, matrix, total_specialists_count, specialists_count_by_group, workplaces_count):
    cost_matrix = make_cost_matrix(matrix)
    munkres = Munkres()
    indexes = munkres.compute(cost_matrix)
    total = 0
    print 'results:'
    for row, column in indexes:
        performance = matrix[row][column]
        specialist_group = get_specialist_group_by_row(row, specialists_count_by_group)
        work = get_work_by_column(column, workplaces_count)
        total += performance / total_specialists_count
        print '(group: %d, work type: %d) -> performance: %f' % (specialist_group, work, performance)
    print 'total max performance = %f' % total


def get_specialist_group_by_row(row, specialists_count_by_group):
	specialists_counter = 0
	group_index = 0
	while row >= specialists_counter:
		group_index += 1
		specialists_counter += specialists_count_by_group[group_index - 1]

	return group_index


def get_work_by_column(column, workplaces_count):
	workplaces_counter = 0
	work_index = 0
	while column >= workplaces_counter:
		work_index += 1
		workplaces_counter += workplaces_count[work_index - 1]

	return work_index


def main():
    m, n, specialists_count_by_group, workplaces_count, specialist_performance_by_group = read_data()
    matrix = make_performance_matrix(m, n, specialists_count_by_group, workplaces_count, specialist_performance_by_group)
    munkres(n, matrix, sum(specialists_count_by_group), specialists_count_by_group, workplaces_count)


if __name__ == '__main__':
    main()
