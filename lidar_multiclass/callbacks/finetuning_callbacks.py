from pytorch_lightning.callbacks import BaseFinetuning


class FinetuningFreezeUnfreeze(BaseFinetuning):
    def __init__(
        self,
        d_in: int = 9,
        num_classes: int = 6,
        unfreeze_decoder_train_epoch: int = None,
    ):
        super().__init__()

        self._d_in = d_in
        self._num_classes = num_classes
        self._unfreeze_decoder_epoch = unfreeze_decoder_train_epoch

    def freeze_before_training(self, pl_module):
        """Update in adn out dimensions and freeze everything at start."""

        # here we could both load the model weights and update its dim afterward
        pl_module.model.update_outer_layers_for_finetuning(
            self._d_in, self._num_classes
        )
        self.freeze(pl_module.model)

    def finetune_function(self, pl_module, current_epoch, optimizer, optimizer_idx):
        """

        Later unfreeze fc_start and bn_start as well.

        """
        if current_epoch == 0:
            self.unfreeze_and_add_param_group(
                modules=pl_module.model.fc_end,
                optimizer=optimizer,
                train_bn=True,
            )
        if current_epoch == self._unfreeze_decoder_epoch:
            self.unfreeze_and_add_param_group(
                modules=pl_module.model.decoder,
                optimizer=optimizer,
                train_bn=True,
            )
