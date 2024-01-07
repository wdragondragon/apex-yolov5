from apex_yolov5.Tools import Tools


def remove_previous_movements(queue, current_quadrant):
    # 从队列中移除之前的不同象限的移动
    index_to_remove = -1
    for i, prev_move in enumerate(queue.queue):
        prev_quadrant = determine_quadrant(prev_move)
        if prev_quadrant != current_quadrant:
            index_to_remove = i

    if index_to_remove >= 0:
        for _ in range(index_to_remove + 1):
            queue.queue.popleft()


def determine_quadrant(move):
    # 确定移动所在的象限
    if move >= 0:
        return 1
    elif move <= 0:
        return -1


queue = Tools.FixedSizeQueue(100)
queue.push(1)
queue.push(-1)
queue.push(1)
queue.push(1)
queue.push(-1)
queue.push(1)
queue.push(-2)
remove_previous_movements(queue, -1)
print(queue.size())
