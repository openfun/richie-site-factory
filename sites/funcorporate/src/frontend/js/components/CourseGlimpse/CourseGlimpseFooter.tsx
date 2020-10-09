import React from 'react';

import { CommonDataProps } from 'richie-education/js/types/commonDataProps';
import { Course } from 'richie-education/js/types/Course';

/**
 * <CourseGlimpseFooter />.
 * This is spun off from <CourseGlimpse /> to allow easier override through webpack.
 */
export const CourseGlimpseFooter: React.FC<{ course: Course } & CommonDataProps> = ({ course }) => (
  <div className="course-glimpse-footer">
    <div className="course-glimpse-footer__date">
      <svg aria-hidden={true} role="img" className="icon">
        <use xlinkHref="#icon-clock" />
      </svg>
      {course.duration}
    </div>
  </div>
);
