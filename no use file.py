grid_coor = [[(325, 172), (325, 262), (325, 352), (325, 442), (325, 532)],
             [(410, 172), (410, 262), (410, 352), (410, 442), (410, 532)],
             [(495, 172), (495, 262), (495, 352), (495, 442), (495, 532)],
             [(586, 172), (586, 262), (586, 352), (586, 442), (586, 532)],
             [(670, 172), (670, 262), (670, 352), (670, 442), (670, 532)]]

event_pos = (671, 500)

def find_grid_coor(event_pos)
    #check at which column (finding coordinate x)
    for i,column in enumerate(grid_coor):
        #cause our grid_coor is center so use + and - to get the max result
        if grid_coor[i][0][0]-42 <= event_pos[0] and grid_coor[i][0][0]+42 >= event_pos[0]:
            # check at which row (finding coordinate y), will output the coor for x and y
            for coor in column:
                if coor[1] -45 <= event_pos[1] and coor[1]+45 >= event_pos[1]:
                    return coor



# [(670, 172), (670, 260), (670, 355), (670, 445), (670, 532)]

# 0 [(325, 172), (325, 260), (325, 355), (325, 445), (325, 532)]
# 1 [(410, 172), (410, 260), (410, 355), (410, 445), (410, 532)]
# 2 [(495, 172), (495, 260), (495, 355), (495, 445), (495, 532)]
# 3 [(586, 172), (586, 260), (586, 355), (586, 445), (586, 532)]
# 4 [(670, 172), (670, 260), (670, 355), (670, 445), (670, 532)]