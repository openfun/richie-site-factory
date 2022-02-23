import type { Maybe } from 'richie-education/js/types/utils';
import { WebAnalyticsAPI } from 'richie-education/js/types/WebAnalytics';
import context from 'richie-education/js/utils/context';
import { handle } from 'richie-education/js/utils/errors/handle';
import FunXitiApi from '../../../../../../js/utils/api/web-analytics/xiti';

const WebAnalyticsAPIHandler = (): Maybe<WebAnalyticsAPI> => {
  try {
    if (context?.web_analytics_provider === 'xiti') {
      return new FunXitiApi();
    }
  } catch (error) {
    handle(error);
  }
  return undefined;
};

export default WebAnalyticsAPIHandler;
