def commandArguments():
  return ['acknowledgeMode','alwaysActivateAllMDBs', 'authenticationAlias', 'autoStopSequentialMessageFailure', 'busName', 'clientId', 'consumerDoesNotModifyPayloadAfterGet', 'description', 'destinationJndiName', 'destinationType', 'durableSubscriptionHome',  'failingMessageDelay', 'forwarderDoesNotModifyPayloadAfterSet', 'jndiName', 'maxBatchSize', 'maxConcurrency', 'messageSelector', 'name', 'providerEndPoints', 'readAhead', 'retryInterval', 'shareDataSourceWithCMP', 'shareDurableSubscriptions', 'subscriptionDurability', 'subscriptionName', 'target', 'targetSignificance', 'targetTransportChain', 'targetType'] 
 
# check if activation spec exists
if asExists(deployed):
# if so .. destroy it
  asDestroy(getId(deployed))


# create activation spec
createJMSActivationSpec(deployed)



