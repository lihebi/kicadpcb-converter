
# Convert KiCAD file to input matrix for routing


- D_PAD
  - GetShape
  - GetPosition
  - GetOrientation
  - GetOrientationDegrees
- PAD_LIST
  - GetNet: crash
- MODULE
  - GetBoundingBox
  - PadsList
  - Pads
  - GetPosition
  - GetOrientation
  - GetReference
  - GetValue
- BOARD
  - Tracks
  - Modules
  - GetNetInfo
  - GetNetCount
  - FindNet(netname/netcode)
  - GetNetsByName
  - GetNetsByNetcode
  - AllConnectedItems
  - GetConnectivity

- BOARD_CONNECTED_ITEM
  - GetNet
  - GetNetCode
  - GetNetname
- CONNECTIVITY_DATA
  - GetNetCount
  - GetConnectedPads


  BOARD

  ```
  ['Add', 'Add3DModel', 'AddNative', 'Back', 'BuildPolyCourtyard', 'CalculateBoundingBox', 'Cast', 'ClassOf', 'ClearAllNets', 'ClearBrightened', 'ClearFlags', 'ClearHighlighted', 'ClearSelected', 'Clone', 'CopyNetlistSettings', 'CoverageRatio', 'Delete', 'DeleteNative', 'DeleteStructure', 'Draw', 'DrawAncre', 'DrawEdgesOnly', 'DrawOutlinesWhenMoving', 'Duplicate', 'FindPadByName', 'Flip', 'GetAllDrawingLayers', 'GetArea', 'GetAttributes', 'GetBoard', 'GetBoundingBox', 'GetBoundingPoly', 'GetCenter', 'GetClass', 'GetDescription', 'GetEditFlags', 'GetFPID', 'GetFlag', 'GetFlags', 'GetFootprintRect', 'GetInitialComments', 'GetKeywords', 'GetLastEditTime', 'GetLayer', 'GetLayerName', 'GetLayerSet', 'GetLink', 'GetList', 'GetLocalClearance', 'GetLocalSolderMaskMargin', 'GetLocalSolderPasteMargin', 'GetLocalSolderPasteMarginRatio', 'GetMenuImage', 'GetMsgPanelInfo', 'GetNextPadName', 'GetOrientation', 'GetOrientationDegrees', 'GetOrientationRadians', 'GetPad', 'GetPadCount', 'GetParent', 'GetPath', 'GetPlacementCost180', 'GetPlacementCost90', 'GetPolyCourtyardBack', 'GetPolyCourtyardFront', 'GetPosition', 'GetReference', 'GetSelectMenuText', 'GetState', 'GetStatus', 'GetThermalGap', 'GetThermalWidth', 'GetTimeStamp', 'GetTopLeftPad', 'GetUniquePadCount', 'GetValue', 'GetZoneConnection', 'GraphicalItems', 'GraphicalItemsList', 'HitTest', 'HitTestAccurate', 'IncrementFlag', 'IncrementReference', 'IsBrightened', 'IsConnected', 'IsDragging', 'IsFlipped', 'IsHighlighted', 'IsLibNameValid', 'IsLocked', 'IsModified', 'IsMoving', 'IsNetTie', 'IsNew', 'IsOnLayer', 'IsPlaced', 'IsReplaceable', 'IsResized', 'IsSelected', 'IsTrack', 'IsType', 'IsWireImage', 'IterateForward', 'Matches', 'Models', 'Move', 'MoveAnchorPosition', 'NeedsPlaced', 'Next', 'Pads', 'PadsList', 'PadsLocked', 'Reference', 'Remove', 'RemoveNative', 'Replace', 'Rotate', 'RunOnChildren', 'SetAttributes', 'SetBrightened', 'SetDescription', 'SetFPID', 'SetFlag', 'SetFlags', 'SetForceVisible', 'SetHighlighted', 'SetInitialComments', 'SetIsPlaced', 'SetKeywords', 'SetLastEditTime', 'SetLayer', 'SetLink', 'SetList', 'SetLocalClearance', 'SetLocalSolderMaskMargin', 'SetLocalSolderPasteMargin', 'SetLocalSolderPasteMarginRatio', 'SetLocked', 'SetModified', 'SetNeedsPlaced', 'SetOrientation', 'SetOrientationDegrees', 'SetPadsLocked', 'SetParent', 'SetPath', 'SetPlacementCost180', 'SetPlacementCost90', 'SetPos', 'SetPosition', 'SetReference', 'SetSelected', 'SetStartEnd', 'SetState', 'SetStatus', 'SetThermalGap', 'SetThermalWidth', 'SetTimeStamp', 'SetValue', 'SetWireImage', 'SetZoneConnection', 'ShowShape', 'Sort', 'StringLibNameInvalidChars', 'SwapData', 'TransformGraphicShapesWithClearanceToPolygonSet', 'TransformGraphicTextWithClearanceToPolygonSet', 'TransformPadsShapesWithClearanceToPolygon', 'TransformShapeWithClearanceToPolygon', 'Type', 'UnLink', 'Value', 'ViewBBox', 'ViewGetLOD', 'ViewGetLayers', 'Visit', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__lt__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__swig_destroy__', '__weakref__', 'this', 'thisown']
  ```