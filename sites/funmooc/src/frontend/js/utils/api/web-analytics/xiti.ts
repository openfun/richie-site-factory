/* eslint-disable class-methods-use-this */
import { BaseWebAnalyticsApi } from 'richie-education/js/utils/api/web-analytics/base';

/**
 *
 * Xiti Richie Web Analytics API Implementation
 *
 * This implementation is used when web analytics is configured as `xiti`.
 * It will send events to the xiti.
 *
 */
export default class FunXitiApi extends BaseWebAnalyticsApi {
  tag: any;

  constructor() {
    super();

    const smartTag = (window as any)?.smartTag;

    // User has denied being tracked or an adblocker has blocked the tag initialization.
    if (smartTag === undefined) {
      return;
    }

    this.tag = smartTag.tag;
  }

  sendEvent(category: string, action: string, label: string): void {
    this.tag?.setProp('s:resource_link', label, false);
    this.tag?.click.send({
      name: category,
      type: 'action',
    });
  }
}
