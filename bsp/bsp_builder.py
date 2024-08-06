from settings import *
from data_types import Segment, BSPNode
from utils import cross_2d


class BSPTreeBuilder:
    def __init__(self, engine):
        self.engine = engine
        # binary search partition root node
        self.root_node = BSPNode()
        #
        self.build_bsp_tree(self.root_node, self.raw_segments)

    def split_space(self, node: BSPNode, input_segments: list[Segment]):
        splitter_seg = input_segments[0]
        splitter_pos = splitter_seg.pos
        splitter_vec = splitter_seg.vector

        node.splitter_vec = splitter_vec
        node.splitter_p0 = splitter_pos[0]
        node.splitter_p1 = splitter_pos[1]

        front_segs, back_segs = [], []

        for segment in input_segments[1:]:
            #
            segment_start = segment.pos[0]
            segment_end = segment.pos[1]
            segment_vector = segment.vector

            numerator = cross_2d((segment_start - splitter_pos[0]), splitter_vec)
            denominator = cross_2d(splitter_vec, segment_vector)

            # if the denominator is zero the lines are parallel
            denominator_is_zero = ads(denominator) < ESP

            # segments are collinear if they are parallel and the numerator is zero
            numerator_is_zero = ads(numerator) < ESP
            #
            if denominator_is_zero and numerator_is_zero:
                front_segs.append(segment)
                continue

    def build_bsp_tree(self, node: BSPNode, input_segments: list[Segment]):
        if not input_segments:
            return None
        #
        front_segs, back_segs = self.split_space(node, input_segments)

        if back_segs:
            node.back = BSPNode()
            self.build_bsp_tree(node.back, back_segs)

        if front_segs:
            node.front = BSPNode()
            self.build_bsp_tree(node.front, front_segs)
