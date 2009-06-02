import hashlib

from casam.models import ModifiedImage


def getModifiedImage(imageRecord, transformation):
  hash = hashlib.sha1(imageRecord.id + transformation).hexdigest()

  try:
    modim = ModifiedImage.objects.select_related().get(hash=hash)
    return modim
  except ModifiedImage.DoesNotExist:
    pass

  properties = dict(
      project=imageRecord.project,
      originalimage=imageRecord,
      transformation=transformation,
      hash=hash,
      )

  modim = ModifiedImage(**properties)
  modim.save()

  return modim
