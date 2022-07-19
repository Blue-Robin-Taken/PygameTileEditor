import pygame
import sys
import os

pygame.init()

# --- Variables ---
ASSET_SIZE = 8

screen = pygame.display.set_mode((384, 216), pygame.RESIZABLE)
screenResize = pygame.surface.Surface((96 * 2, 54 * 2))

assetList = []
selectAssetList = []
returnList = []


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self.position = position

    def update(self, offset):
        self.rect.x = offset[0] + self.position[0]
        self.rect.y = offset[1] + self.position[1]


def getAssets():
    global assetList

    for asset in os.listdir(os.path.relpath("assets")):
        assetList.append(pygame.image.load(os.path.relpath("assets/" + asset)).convert_alpha())


def getSelectAssets():
    global selectAssetList
    for asset in os.listdir(os.path.relpath("assets")):
        selectAssetList.append(pygame.image.load(os.path.relpath("assets/" + asset)).convert_alpha())

    for asset in selectAssetList:
        asset.set_alpha(100)


# --- Main game loop ---
def main():
    alive = True
    selectedAsset = 0

    tileGroup = pygame.sprite.Group()
    camOffsetX = 0
    camOffsetY = 0
    selectedTile = Tile(selectAssetList[selectedAsset], (camOffsetX, camOffsetY))

    while alive:
        getKeys = pygame.key.get_pressed()

        mouse_pos = (
            ((pygame.mouse.get_pos()[0]) * (screenResize.get_width() / screen.get_width())) - ASSET_SIZE / 2,
            ((pygame.mouse.get_pos()[1]) * (screenResize.get_height() / screen.get_height())) - ASSET_SIZE / 2)
        # Note: The ASSET_SIZE/2 is to center the tile position to the mouse
        # Note: * (screenResize.get_height() / screen.get_height())) is to get the ratio
        tilePos = (round((mouse_pos[0] - camOffsetX) / ASSET_SIZE) * ASSET_SIZE,
                   round((mouse_pos[1] - camOffsetY) / ASSET_SIZE) * ASSET_SIZE)  # calculate the tile position
        tilePosSelect = (round((mouse_pos[0]) / ASSET_SIZE) * ASSET_SIZE,
                         round((mouse_pos[1]) / ASSET_SIZE) * ASSET_SIZE)

        previousMousePos = pygame.mouse.get_pos()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2:
                    print(returnList)
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[2]:  # Right button pressed
                    selectedAsset += 1
                    if selectedAsset >= len(assetList):
                        selectedAsset = 0
                    selectedTile = Tile(selectAssetList[selectedAsset], (0, 0))
        if pygame.mouse.get_pressed()[1] or pygame.mouse.get_pressed()[0] and (
                not getKeys[pygame.K_LCTRL]):  # Middle button pressed or left button pressed
            for asset in range(len(assetList)):
                if [asset, (tilePos[0], tilePos[1])] in returnList:
                    returnList.remove([asset, (tilePos[0], tilePos[1])])
                    for tile in tileGroup:
                        if (tile.rect.x, tile.rect.y) == tilePos:
                            tile.kill()
        if pygame.mouse.get_pressed()[0] and (not getKeys[pygame.K_LCTRL]):  # Left button pressed
            duplicate = False
            for i in returnList:
                for asset in range(len(assetList)):
                    if i == [asset,
                             (tilePos[0],
                              tilePos[1])]:  # The list is formatted like so:[The asset, the position]
                        duplicate = True
            if not duplicate:
                tileGroup.add(Tile(assetList[selectedAsset], (tilePos[0], tilePos[1])))

                returnList.append([selectedAsset,
                                   (tilePos[0], tilePos[1])])

        if pygame.mouse.get_pressed()[0] and getKeys[pygame.K_LCTRL]:
            camOffsetX -= previousMousePos[0] - pygame.mouse.get_pos()[0]
            camOffsetY -= previousMousePos[1] - pygame.mouse.get_pos()[1]

        screenResize.fill((0, 0, 0))

        tileGroup.update((camOffsetX, camOffsetY))
        tileGroup.draw(screenResize)
        selectedTile.kill()
        selectedTile = Tile(selectAssetList[selectedAsset], (tilePos[0], tilePos[1]))
        selectedTile.update((camOffsetX, camOffsetY))

        # selectedTile.update((round(camOffsetX / ASSET_SIZE), round(camOffsetY / ASSET_SIZE)))
        screenResize.blit(selectedTile.image, (selectedTile.rect.x, selectedTile.rect.y))

        screen.blit(pygame.transform.scale(screenResize, (screen.get_width(), screen.get_height())), (0, 0))

        pygame.display.update()


if __name__ == '__main__':
    getAssets()
    getSelectAssets()
    main()
